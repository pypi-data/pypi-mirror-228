import dataclasses as dc
import itertools
import typing as t

import tqdm
from overrides import override

import superduperdb as s
from superduperdb import logging
from superduperdb.container.component import Component
from superduperdb.container.document import Document
from superduperdb.container.encoder import Encodable
from superduperdb.container.listener import Listener
from superduperdb.db.base.db import DB
from superduperdb.misc.special_dicts import MongoStyleDict
from superduperdb.vector_search.base import (
    VectorCollectionConfig,
    VectorCollectionItem,
    VectorIndexMeasureType,
)

if t.TYPE_CHECKING:
    pass

T = t.TypeVar('T')


def ibatch(iterable: t.Iterable[T], batch_size: int) -> t.Iterator[t.List[T]]:
    """
    Batch an iterable into chunks of size `batch_size`

    :param iterable: the iterable to batch
    :param batch_size: the number of groups to write
    """
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch


@dc.dataclass
class VectorIndex(Component):
    """A component representing a VectorIndex"""

    #: Unique string identifier of index
    identifier: str

    #: Listener which is applied to created vectors
    indexing_listener: t.Union[Listener, str]

    #: List of additional listeners which can "talk" to the index (e.g. multi-modal)
    compatible_listener: t.Union[None, Listener, str] = None

    #: Measure which is used to compare vectors in index
    measure: VectorIndexMeasureType = VectorIndexMeasureType.cosine

    #: A version number for the index (unused)
    version: t.Optional[int] = None

    #: Metric values used for training
    metric_values: t.Optional[t.Dict] = dc.field(default_factory=dict)

    #: A unique name for the class
    type_id: t.ClassVar[str] = 'vector_index'

    @override
    def on_create(self, db: DB) -> None:
        if isinstance(self.indexing_listener, str):
            self.indexing_listener = t.cast(
                Listener, db.load('listener', self.indexing_listener)
            )

        if isinstance(self.compatible_listener, str):
            self.compatible_listener = t.cast(
                Listener, db.load('listener', self.compatible_listener)
            )

        if getattr(s.CFG.vector_search.type, 'selfhosted', False):
            if (create := getattr(db.databackend, 'create_vector_index', None)) is None:
                msg = 'VectorIndex is not supported by the current database backend'
                raise ValueError(msg)

            create(self)

    @override
    def on_load(self, db: DB) -> None:
        if not getattr(s.CFG.vector_search.type, 'selfhosted', False):
            assert db.vector_database
            self.vector_table = db.vector_database.get_table(
                VectorCollectionConfig(
                    id=self.identifier,
                    dimensions=self.dimensions,
                    measure=self.measure,
                ),
                create=True,  # type: ignore[call-arg]
            )

        if not s.CFG.cdc:
            self._initialize_vector_database(db)

    @property
    def child_components(self) -> t.Sequence[t.Tuple[str, str]]:
        out = [('indexing_listener', 'listener')]
        if self.compatible_listener is not None:
            out.append(('compatible_listener', 'listener'))
        return out

    def get_vector(
        self,
        like: Document,
        models: t.List[str],
        keys: t.List[str],
        db: t.Any = None,
        outputs: t.Optional[t.Dict] = None,
        featurize: bool = True,
    ):
        document = MongoStyleDict(like.unpack())
        if featurize:
            outputs = outputs or {}
            if '_outputs' not in document:
                document['_outputs'] = {}
            document['_outputs'].update(outputs)

            assert not isinstance(self.indexing_listener, str)
            features = self.indexing_listener.features or ()
            for subkey in features:
                subout = document['_outputs'].setdefault(subkey, {})
                f_subkey = features[subkey]
                if f_subkey not in subout:
                    subout[f_subkey] = db.models[f_subkey]._predict(document[subkey])
                document[subkey] = subout[f_subkey]
        available_keys = list(document.keys()) + ['_base']
        try:
            model_name, key = next(
                (m, k) for m, k in zip(models, keys) if k in available_keys
            )
        except StopIteration:
            raise Exception(
                f'Keys in provided {like} don\'t match'
                f' VectorIndex keys: {keys}, with model: {models}'
            )
        model_input = document[key] if key != '_base' else document
        model = db.models[model_name]
        return model.predict(model_input, one=True), model.identifier, key

    def get_nearest(
        self,
        like: Document,
        db: t.Any = None,
        outputs: t.Optional[t.Dict] = None,
        featurize: bool = True,
        ids: t.Optional[t.Sequence[str]] = None,
        n: int = 100,
    ) -> t.Tuple[t.List[str], t.List[float]]:
        """Given a document, find the nearest results in this vector index, returned as
        two parallel lists of result IDs and scores

        :param like: The document to compare against
        :param db: The datastore to use
        :param outputs: An optional dictionary
        :param featurize: Enable featurization
        :param ids: A list of ids to match
        :param n: Number of items to return
        """
        models, keys = self.models_keys
        if len(models) != len(keys):
            raise ValueError(f'len(model={models}) != len(keys={keys})')
        within_ids = ids or ()

        if isinstance(like.content, dict) and db.db.id_field in like.content:
            nearest = self.vector_table.find_nearest_from_id(
                str(like[db.db.id_field]), within_ids=within_ids, limit=n
            )
            return (
                [result.id for result in nearest],
                [result.score for result in nearest],
            )
        h = self.get_vector(
            like=like,
            models=models,
            keys=keys,
            db=db,
            outputs=outputs,
            featurize=featurize,
        )[0]
        nearest = self.vector_table.find_nearest_from_array(
            h, within_ids=within_ids, limit=n
        )
        return (
            [result.id for result in nearest],
            [result.score for result in nearest],
        )

    @property
    def models_keys(self) -> t.Tuple[t.List[str], t.List[str]]:
        """
        Return a list of model and keys for each listener
        """
        assert not isinstance(self.indexing_listener, str)
        assert not isinstance(self.compatible_listener, str)

        if self.compatible_listener:
            listeners = [self.indexing_listener, self.compatible_listener]
        else:
            listeners = [self.indexing_listener]

        models = [
            w.model.identifier  # type: ignore[assignment, identifier, union-attr]
            for w in listeners
        ]
        keys = [w.key for w in listeners]
        return models, keys

    def _initialize_vector_database(self, db: DB) -> None:
        logging.info(f'loading hashes: {self.identifier!r}')
        assert not isinstance(self.indexing_listener, str)

        if self.indexing_listener.select is None:
            raise ValueError('.select must be set')

        progress = tqdm.tqdm(desc='Loading vectors into vector-table...')
        for record_batch in ibatch(
            db.execute(self.indexing_listener.select),
            s.CFG.vector_search.backfill_batch_size,
        ):
            items = []
            for record in record_batch:
                key = self.indexing_listener.key
                if key.startswith('_outputs.'):
                    key = key.split('.')[1]

                id = record[db.databackend.id_field]
                assert not isinstance(self.indexing_listener.model, str)
                h = record.outputs(key, self.indexing_listener.model.identifier)
                if isinstance(h, Encodable):
                    h = h.x
                items.append(VectorCollectionItem.create(id=str(id), vector=h))

            self.vector_table.add(items)
            progress.update(len(items))

    @property
    def dimensions(self) -> int:
        assert not isinstance(self.indexing_listener, str)
        assert not isinstance(self.indexing_listener.model, str)
        if shape := getattr(self.indexing_listener.model.encoder, 'shape', None):
            return shape[-1]
        raise ValueError('Couldn\'t get shape of model outputs from model encoder')
