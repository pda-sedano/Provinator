from alter_provinces import Provinator


if __name__ == '__main__':
    provinator = Provinator(
        provinces_folder = '/Users/gsvboti/Library/Application Support/Steam/steamapps/common/Europa Universalis IV/history/provinces',
        province_ids = [
            490, 2658, 2659, 4620, 4621, 486, 2654, 2655, 2656, 481, 487, 491, 492, 488, 489, 4618, 4619, 493, 494, 495, 
            496, 1881, 482, 483, 484, 485, 4622, 4623, 4624, 497, 498, 499, 500, 501
        ],
        patterns_to_search = [("trade_goods", "slaves")],
        new_owner = 'HSS',
        keywords = ["owner", "controller", "add_core", "culture"],
        block_to_append_keyword= "discovered_by"
    )

    provinator.provinate()

    print("Yoho! yoho! A pirate's life for me")
