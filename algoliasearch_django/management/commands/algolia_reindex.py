from django.core.management.base import BaseCommand

from algoliasearch_django import get_registered_model
from algoliasearch_django import reindex_all


class Command(BaseCommand):
    help = 'Reindex all models to Algolia'

    def add_arguments(self, parser):
        parser.add_argument('--batchsize', nargs='?', default=1000, type=int)
        parser.add_argument('--model', nargs='+', type=str)
        parser.add_argument('--unified', action='store_true', help="Models will use a common index.")

    def handle(self, *args, **options):
        """Run the management command."""
        batch_size = options.get('batchsize', None)
        if not batch_size:
            # py34-django18: batchsize is set to None if the user don't set
            # the value, instead of not be present in the dict
            batch_size = 1000

        if options.get('unified', None):
            models = get_registered_model()
            model = models.pop(0)
            counts = reindex_all(model, batch_size=batch_size, extra_models=models)
            self.stdout.write('Unified {} models with {} items'.format(len(models), counts))
        else:
            self.stdout.write('The following models were reindexed:')
            for model in get_registered_model():
                if options.get('model', None) and not (model.__name__ in
                                                       options['model']):
                    continue

                counts = reindex_all(model, batch_size=batch_size)
                self.stdout.write('\t* {} --> {}'.format(model.__name__, counts))
