from __future__ import annotations
import datetime
from django.db.models.query import QuerySet
from ..models import Airport, Metar


class AirportMetarNewest():
    """Get and store the newest datetime of the METAR of the airports.

    The datetimes are stored as dict: key is station_id, value is
    observation_time.

    Attributes:
        airport_list (list[str]): List of airports to be searched the newest.
        newest_dict (dict[str: datetime]): station_id and the datetime.
    """
    def __init__(self) -> None:
        self.__airport_list = get_airport_list()
        self.__newest_dict = {}
        metar_dict = self.__get_newest().values('station_id', 'observation_time')
        for airport in metar_dict:
            self.__newest_dict[airport['station_id']] = airport['observation_time']

    @property
    def airport_list(self) -> list[str]:
        return self.__airport_list

    @property
    def newest_dict(self) -> dict[str: datetime]:
        return self.__newest_dict

    def __get_newest(self) -> QuerySet:
        """Get QuerySet object of the newest data.

        Returns:
            QuerySet: QuerySet from Metar model.
        """
        metar_query = Metar.objects \
            .filter(
                station_id__in=self.__airport_list
            ) \
            .order_by(
                'observation_time'
            ) \
            .reverse()[:1]
        return metar_query


def get_airport_list() -> list[str]:
    """Get list of aiport ICAO ids from database

    Returns:
        list[str]: Stored ICAO ids for fetching METAR.
    """
    airport_list_query = Airport.objects \
        .filter(
            is_fetched=True
        ) \
        .values_list('station_id', flat=True)
    airport_list = list(airport_list_query)
    return airport_list
