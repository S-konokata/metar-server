import argparse
from django.core.management.base import BaseCommand, CommandParser
from typing import Any, Optional
from ...myfunction import airport_function, metar_function


class Command(BaseCommand):
    help = 'Fetch METAR data and save to database.'

    def add_arguments(self, parser: CommandParser):
        """Add argument '--hour' for MetarInput.hour
        """
        parser.add_argument(
            '--hour',
            action='store',
            type=self.__valid_arg_hour,
            required=False,
            help='Hours before now for fetching METAR, The maximum value is 72',
            dest='hour'
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Command of fetching and saving METARs.

        Returns:
            Optional[str]: Options for inherited function.
        """
        airport_list = airport_function.get_airport_list()
        metar_input = metar_function.MetarInput(airport_list)
        if options['hour'] is not None:
            metar_input.hour = options['hour']
        metar_input.fetch_and_save()
        self.stdout.write('Fetched airport is %s' % airport_list)
        self.stdout.write('Fetched time is %s' % metar_input.fetched_time)
        self.stdout.write('The number of the fetched data is %s' % len(metar_input.fetched_data))

    def __valid_arg_hour(self, myarg) -> int:
        """Validation of '--hour' argument of the command.

        Args:
            myarg (Any): Input argument.

        Raises:
            argparse.ArgumentTypeError: Raises if the input is not between
                1 and 72.
            argparse.ArgumentTypeError: Raises if the input is not value.

        Returns:
            int: int of the input.
        """
        try:
            outvalue = int(myarg)
            if 1 <= outvalue <= 72:
                return outvalue
            raise argparse.ArgumentTypeError('The value should be between 1 and 72, but %s is given.'
                                             % outvalue)
        except ValueError:
            raise argparse.ArgumentTypeError('%s is not integer' % myarg)
