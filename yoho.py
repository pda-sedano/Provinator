from pathlib import Path
from Provinator.alterations.add_or_update_equals import AddOrUpdateEquals
from Provinator.filters.equals_filter import EqualsFilter
from Provinator.filters.province_id_filter import ProvinceIdFilter
from Provinator.provinator import Provinator


if __name__ == '__main__':
    provinces_folder = '/Users/gsvboti/Library/Application Support/Steam/steamapps/common/Europa Universalis IV/history/provinces'

    provinator = Provinator(
        provinces_folder=Path(provinces_folder),
        filter_mode='or',
    )
    provinator.add_filter(ProvinceIdFilter(ids=[
            490, 2658, 2659, 4620, 4621, 486, 2654, 2655, 2656, 481, 487, 491, 492, 488, 489, 4618, 4619, 493, 494, 495, 
            496, 1881, 482, 483, 484, 485, 4622, 4623, 4624, 497, 498, 499, 500, 501
        ]))
    provinator.add_filter(EqualsFilter(patterns=[('trade_goods', 'slaves')]))
    provinator.add_alteration(AddOrUpdateEquals(patterns=[
        ('owner', 'HSS'),
        ('controller', 'HSS'),
        ('add_core', 'HSS'),
        ('culture', 'HSS'),
        ('trade_goods', 'gold'),
    ], block_append_keyword='discovered_by'))

    provinator.provinate()

    print("Yoho! yoho! A pirate's life for me")
