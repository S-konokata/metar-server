from __future__ import annotations
from datetime import datetime, timedelta
from django.db.models.query import QuerySet
from django.utils import dateparse, timezone
from defusedxml.ElementTree import fromstring
import re
import requests
from xml.etree.ElementTree import Element, ElementTree
from ..models import Metar


class MetarInput():
    """Class for getting Metar model classes from AWC server.

    If METAR data more/less 25 hours from fetched time is required,
    'hour' attribute should be set.

    Attributes:
        airport_list (list[str]): List of airports to be fetched.
        hour (int): hoursBeforeNow for fetching URL.
        fetched_time (datetime): Datetime when fetching the METAR data.
        fetched_data (list[Metar]): Metar models from get_models method.
    """
    def __init__(self, airport_list: list[str], hour: int = 25) -> None:
        self.airport_list = airport_list
        self.hour = hour
        self.fetched_time: datetime = None
        self.fetched_data: list[Metar] = []

    def fetch_and_save(self):
        """Get METAR data and save to database.
        """
        self.get_models()
        Metar.objects.bulk_create(self.fetched_data, 100)

    def get_models(self) -> list[Metar]:
        """Get METAR data and convert to list of Metar instance(s).

        Returns:
            list[Metar]: List of Metar model instance(s) used for Django ORM.
        """
        fetched_et = self.__fetch_metar()
        metar_elements = fetched_et.findall('./data/METAR')
        store_recent = self.__get_recent()
        for element in metar_elements:
            metar_model = self.__get_single_model(element)
            if self.__is_duplicate(metar_model, store_recent) is True:
                continue
            else:
                self.fetched_data.append(metar_model)
        return self.fetched_data

    def __fetch_metar(self) -> ElementTree:
        """Fetched XML data of METAR. Returns as ElementTree of the XML.

        The METAR data is fetched from Aviation Weather Center.

        Returns:
            ElementTree: ElementTree of th fetched XML data.
        """
        URL = r'https://www.aviationweather.gov/adds/dataserver_current/httpparam'
        payload = {
            'dataSource': 'metars',
            'requestType': 'retrieve',
            'format': 'xml',
            'stationString': ','.join(self.airport_list),
            'hoursBeforeNow': str(self.hour)
        }
        res = requests.get(URL, params=payload)
        self.fetched_time = timezone.now()
        et = fromstring(res.text, forbid_dtd=True)
        return et

    def __get_single_model(self, element: Element) -> Metar:
        """Create Metar instance from Element of XML data.

        Args:
            element (Element): Element of 'METAR' section in the XML.

        Returns:
            Metar: Metar model of Django ORM.

        Raises:
            re.error: if visibility_m is not found.
        """
        VIS_RE = r'KT ([0-9]{3}V[0-9]{3} )?(?P<vis>[0-9]{4})'
        VIS_CAVOK_RE = r'KT ([0-9]{3}V[0-9]{3} )?CAVOK'
        raw_text = element.findtext('raw_text')
        station_id = element.findtext('station_id')
        datetime_rawtext = element.findtext('observation_time')
        observation_time = dateparse.parse_datetime(datetime_rawtext)
        temp_c = float(element.findtext('temp_c'))
        dewpoint_c = float(element.findtext('dewpoint_c'))
        wind_dir_degrees = int(element.findtext('wind_dir_degrees'))
        wind_speed_kt = int(element.findtext('wind_speed_kt'))
        altim_in_hg = float(element.findtext('altim_in_hg'))
        metar_type = element.findtext('metar_type')

        metar = Metar(
            raw_text=raw_text,
            station_id=station_id,
            observation_time=observation_time,
            temp_c=temp_c,
            dewpoint_c=dewpoint_c,
            wind_dir_degrees=wind_dir_degrees,
            wind_speed_kt=wind_speed_kt,
            altim_in_hg=altim_in_hg,
            metar_type=metar_type
        )

        try:
            vis_match = re.search(VIS_RE, raw_text).group('vis')
            visibility_m = int(vis_match)
        except AttributeError:
            if re.search(VIS_CAVOK_RE, raw_text) is not None:
                visibility_m = 9999
            else:
                raise re.error('visibility is not found in raw text: %s' % raw_text)
        metar.visibility_m = visibility_m

        if element.findtext('wind_gust_kt') is not None:
            wind_gust_kt = int(element.findtext('wind_gust_kt'))
            metar.wind_gust_kt = wind_gust_kt

        if element.findtext('wx_string') is not None:
            wx_string = element.findtext('wx_string')
            metar.wx_string = wx_string

        for child in element.iter():
            if 'sky_cover' in child.attrib and child.attrib['sky_cover'] == 'BKN':
                cloud_ceiling = int(child.attrib['cloud_base_ft_agl'])
                metar.cloud_ceiling = cloud_ceiling
                break

        if element.findtext('vert_vis_ft') is not None:
            vert_vis_ft = int(element.findtext('vert_vis_ft'))
            metar.vert_vis_ft = vert_vis_ft

        return metar

    def __is_duplicate(self, metar: Metar, store_recent: QuerySet) -> bool:
        """Check whether Metar object is in recent data.

        Args:
            metar (Metar): Metar model for the check.
            store_recent (QuerySet): recent data form __get_recent.

        Returns:
            bool: Returns True if metar is in store_recent.
        """
        for stored in store_recent.values():
            if (stored['station_id'] == metar.station_id and
                    stored['observation_time'] == metar.observation_time):
                return True
        return False

    def __get_recent(self) -> QuerySet:
        """Get recent METAR records from database for checking duplicated.

        Returns:
            QuerySet: Filtered QuerySet from database.
        """
        recent_datetime = self.fetched_time - timedelta(hours=73)
        store_recent = Metar.objects \
            .filter(
                observation_time__gte=recent_datetime
            )
        return store_recent
