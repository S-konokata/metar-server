from __future__ import annotations
import datetime
from defusedxml.ElementTree import parse
import re
import requests
from xml.etree.ElementTree import Element, ElementTree
from ..models import Metar


class MetarInput():
    """Class for getting Metar model classes from AWS server.

    Attributes:
        airport_list: 
    """
    def __init__(self, airport_list: list[str]) -> None:
        self.airport_list = airport_list

    def get_models(self) -> list[Metar]:
        fetched_et = self.__fetch_metar()
        metar_elements = fetched_et.findall('./data/METAR')
        outlist: list[Metar] = []
        for element in metar_elements:
            outlist.append(self.__get_single_model(element))
        return outlist

    def __fetch_metar(self) -> ElementTree:
        URL = r'https://www.aviationweather.gov/adds/dataserver_current/httpparam'
        payload = {
            'dataSource': 'metars',
            'requestType': 'retrieve',
            'format': 'xml',
            'stationString': ','.join(self.airport_list),
            'hoursBeforeNow': '25'
        }
        res = requests.get(URL, params=payload)
        et = parse(res, forbid_dtd=True)
        return et

    def __get_single_model(self, element: Element) -> Metar:
        VIS_RE = r'KT ([0-9]{3}V[0-9]{3} )?(?P<vis>[0-9]{4})'
        raw_text = element.findtext('raw_text')
        station_id = element.findtext('station_id')
        datetime_rawtext = element.findtext('observation_time')
        # Remove last "Z" from datetime string.
        observation_time = datetime.datetime.fromisoformat(datetime_rawtext[:-1])
        temp_c = float(element.findtext('temp_c'))
        dewpoint_c = float(element.findtext('dewpoint_c'))
        wind_dir_degrees = int(element.findtext('wind_dir_degrees'))
        wind_speed_kt = int(element.findtext('wind_speed_kt'))
        visibility_m = int(re.search(VIS_RE, raw_text).group('vis'))
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
            visibility_m=visibility_m,
            altim_in_hg=altim_in_hg,
            metar_type=metar_type
        )

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
