# -*- coding: utf-8 -*-
import json

tree_data = {
    "title": "Arbre Généalogique de la Famille - Descendance d'Ibrahim",
    "root": {
        "id": "ibrahim_0",
        "name": "Ibrahim",
        "role": "Patriarche / Ancêtre Fondateur",
        "gen": 1,
        "branch": "root",
        "dates": "",
        "notes": "",
        "children_branches": [
            {
                "branch_name": "Branche Adem",
                "branch_color": "emerald", # Emerald / Vert Sauge
                "id": "adem_branch",
                "person": {
                    "id": "adem_1",
                    "name": "Adem",
                    "dates": "1855 – 1938",
                    "notes": "",
                    "gen": 2,
                    "spouse": {
                        "name": "Mejra",
                        "dates": "",
                        "notes": "Supruga"
                    },
                    "children": [
                        {
                            "id": "avdo_adem",
                            "name": "Avdo",
                            "dates": "1887 – 1957",
                            "gen": 3,
                            "spouse": {"name": "Azemina", "notes": "r. Husejnović"},
                            "children": [
                                {"id": "osman_avdo_adem", "name": "Osman", "dates": "", "notes": "n. Poginuo", "gen": 4},
                                {"id": "nurija_avdo_adem", "name": "Nurija", "dates": "", "notes": "n. Poginuo", "gen": 4},
                                {"id": "hatidza_avdo_adem", "name": "Hatidza", "dates": "", "notes": "", "gen": 4},
                                {
                                    "id": "beriz_avdo_adem", "name": "Beriz", "dates": "", "gen": 4,
                                    "spouse": {"name": "Nura", "notes": "Supruga"},
                                    "children": [
                                        {"id": "seida_beriz", "name": "Seida", "gen": 5},
                                        {"id": "bahrija_beriz", "name": "Bahrija", "gen": 5},
                                        {"id": "hatidza_beriz", "name": "Hatidža", "gen": 5},
                                        {"id": "zemina_beriz", "name": "Zemina", "gen": 5},
                                        {
                                            "id": "dzevad_beriz", "name": "Dževad", "gen": 5,
                                            "children": [
                                                {"id": "beriz_dzevad", "name": "Beriz", "gen": 6},
                                                {"id": "nedzad_dzevad", "name": "Nedžad", "gen": 6}
                                            ]
                                        },
                                        {"id": "halida_beriz", "name": "Halida", "gen": 5},
                                        {
                                            "id": "nesad_beriz", "name": "Nešad", "gen": 5,
                                            "children": [
                                                {"id": "azra_nesad", "name": "Azra", "gen": 6},
                                                {"id": "almedina_nesad", "name": "Almedina", "gen": 6},
                                                {"id": "kenan_nesad", "name": "Kenan", "gen": 6},
                                                {"id": "dzenan_nesad", "name": "Dženan", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "mujo_adem",
                            "name": "Mujo",
                            "dates": "1897 – 1934",
                            "gen": 3,
                            "spouse": {"name": "Šemsa", "notes": "r. Husejnovca"},
                            "children": [
                                {
                                    "id": "husnija_mujo", "name": "Husnija", "dates": "1925 – 1988", "gen": 4,
                                    "spouse": {"name": "Sajda", "dates": "1926 – 1999", "notes": "r. Čilašević"},
                                    "children": [
                                        {
                                            "id": "fahrudin_husnija", "name": "Fahrudin", "gen": 5,
                                            "spouse": {"name": "Mulfeta", "notes": "r. Sniježnica"},
                                            "children": [
                                                {
                                                    "id": "zaim_fahrudin", "name": "Zaim", "gen": 6,
                                                    "spouse": {"name": "Samra", "notes": "r. Glinje"},
                                                    "children": [{"id": "armin_zaim", "name": "Armin", "gen": 7}]
                                                },
                                                {"id": "emina_fahrudin", "name": "Emina", "gen": 6},
                                                {
                                                    "id": "vahidin_fahrudin", "name": "Vahidin", "gen": 6,
                                                    "spouse": {"name": "Nedžmira", "notes": "Supruga"},
                                                    "children": [
                                                        {"id": "esma_vahidin", "name": "Esma", "gen": 7},
                                                        {"id": "sajda_vahidin", "name": "Sajda", "gen": 7}
                                                    ]
                                                },
                                                {
                                                    "id": "adnan_fahrudin", "name": "Adnan", "gen": 6,
                                                    "spouse": {"name": "Mirela", "notes": "Supruga"},
                                                    "children": [
                                                        {"id": "adel_adnan", "name": "Adel", "gen": 7},
                                                        {"id": "meliha_adnan", "name": "Meliha", "gen": 7},
                                                        {"id": "vedad_adnan", "name": "Vedad", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        },
                                        {"id": "semsa_husnija", "name": "Šemsa", "notes": "u. Bilalić", "gen": 5},
                                        {"id": "zurijeta_husnija", "name": "Zurijeta", "notes": "u. Hadžić", "gen": 5},
                                        {"id": "nura_husnija", "name": "Nura", "notes": "u. Aljić", "gen": 5},
                                        {"id": "mensura_husnija", "name": "Mensura", "notes": "u. Omerović", "gen": 5},
                                        {"id": "izeta_husnija", "name": "Izeta", "notes": "u. Murtić", "gen": 5},
                                        {"id": "hatidza_husnija", "name": "Hatidža", "notes": "u. Redžić", "gen": 5},
                                        {"id": "fatima_husnija", "name": "Fatima", "notes": "u. Alić", "gen": 5},
                                        {
                                            "id": "kadraga_husnija", "name": "Kadraga", "gen": 5,
                                            "spouse": {"name": "Zekira", "notes": "r. Janja"},
                                            "children": [
                                                {
                                                    "id": "azra_kadraga", "name": "Azra", "notes": "r. Zehić", "gen": 6,
                                                    "spouse": {"name": "Mirza Halilović", "notes": "Suprug"},
                                                    "children": [{"id": "hamza_mirza", "name": "Hamza", "gen": 7}]
                                                },
                                                {
                                                    "id": "samir_kadraga", "name": "Samir", "gen": 6,
                                                    "spouse": {"name": "Merima", "notes": "Supruga"},
                                                    "children": [{"id": "adna_samir", "name": "Adna", "gen": 7}]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": "hadzaga_mujo", "name": "Hadžaga", "gen": 4,
                                    "spouse": {"name": "Zarfa", "notes": "r. T. Brdo"},
                                    "children": [
                                        {
                                            "id": "sadik_hadzaga", "name": "Sadik", "gen": 5,
                                            "children": [
                                                {"id": "meliha_sadik", "name": "Meliha", "gen": 6},
                                                {"id": "hido_sadik", "name": "Hido", "gen": 6}
                                            ]
                                        },
                                        {"id": "zlatka_hadzaga", "name": "Zlatka", "gen": 5},
                                        {"id": "sadika_hadzaga", "name": "Sadika", "gen": 5},
                                        {"id": "mineta_hadzaga", "name": "Mineta", "gen": 5},
                                        {
                                            "id": "asmir_hadzaga", "name": "Asmir", "gen": 5,
                                            "children": [
                                                {"id": "amra_asmir", "name": "Amra", "gen": 6},
                                                {"id": "amir_asmir", "name": "Amir", "gen": 6}
                                            ]
                                        },
                                        {"id": "azra_hadzaga", "name": "Azra", "gen": 5},
                                        {"id": "zikreta_hadzaga", "name": "Zikreta", "gen": 5}
                                    ]
                                },
                                {"id": "saban_mujo", "name": "Šaban", "gen": 4},
                                {"id": "dzemila_mujo", "name": "Džemila", "gen": 4},
                                {
                                    "id": "harnaga_mujo", "name": "Harnaga", "gen": 4,
                                    "spouse": {"name": "Hatidža", "notes": "Supruga"},
                                    "children": [
                                        {"id": "halida_harnaga", "name": "Halida", "notes": "u. Smajić", "gen": 5},
                                        {"id": "dzemila_harnaga", "name": "Džemila", "notes": "u. Haić", "gen": 5},
                                        {"id": "izeta_harnaga", "name": "Izeta", "gen": 5},
                                        {
                                            "id": "izet_harnaga", "name": "Izet", "gen": 5,
                                            "children": [
                                                {
                                                    "id": "admir_izet_h", "name": "Admir", "gen": 6,
                                                    "children": [
                                                        {"id": "emrah_admir_h", "name": "Emrah", "gen": 7},
                                                        {"id": "emina_admir_h", "name": "Emina", "gen": 7}
                                                    ]
                                                },
                                                {"id": "sabina_izet_h", "name": "Sabina", "gen": 6},
                                                {"id": "emina_izet_h", "name": "Emina", "gen": 6},
                                                {
                                                    "id": "haris_izet_h", "name": "Haris", "gen": 6,
                                                    "children": [
                                                        {"id": "benjamin_haris", "name": "Benjamin", "gen": 7},
                                                        {"id": "hana_haris", "name": "Hana", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "sajtan_adem", "name": "Sajtan", "gen": 3,
                            "spouse": {"name": "Zemina", "notes": "r. Bešići"},
                            "children": [
                                {
                                    "id": "began_sajtan", "name": "Began", "gen": 4,
                                    "spouse": {"name": "Zilka", "notes": "Supruga"},
                                    "children": [
                                        {"id": "begajeta_began", "name": "Begajeta", "gen": 5},
                                        {"id": "biba_began", "name": "Biba", "gen": 5},
                                        {
                                            "id": "sefik_began", "name": "Šefik", "gen": 5,
                                            "children": [
                                                {"id": "amela_sefik", "name": "Amela", "gen": 6},
                                                {"id": "jasmin_sefik", "name": "Jasmin", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": "mustafa_sajtan", "name": "Mustafa", "gen": 4,
                                    "spouse": {"name": "Šuhra", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "saban_mustafa", "name": "Šaban", "gen": 5,
                                            "children": [
                                                {"id": "azra_saban_m", "name": "Azra", "gen": 6},
                                                {"id": "aida_saban_m", "name": "Aida", "gen": 6}
                                            ]
                                        },
                                        {"id": "zemina_mustafa", "name": "Zemina", "gen": 5},
                                        {"id": "hasiba_mustafa", "name": "Hasiba", "gen": 5},
                                        {"id": "sumbila_mustafa", "name": "Sumbila", "gen": 5},
                                        {"id": "sena_mustafa", "name": "Sena", "gen": 5},
                                        {
                                            "id": "bekrija_mustafa", "name": "Bekrija", "gen": 5,
                                            "children": [
                                                {"id": "selma_bekrija", "name": "Selma", "gen": 6},
                                                {"id": "vahida_bekrija", "name": "Vahida", "gen": 6},
                                                {"id": "vahidin_bekrija", "name": "Vahidin", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {"id": "kcerka_sajtan", "name": "Kćerka", "gen": 4, "notes": "(Non nommée)"},
                                {"id": "fata_sajtan", "name": "Fata", "gen": 4},
                                {
                                    "id": "ismet_sajtan", "name": "Ismet", "gen": 4,
                                    "spouse": {"name": "Hajrija", "notes": "Supruga"}
                                },
                                {"id": "selima_sajtan", "name": "Selima", "gen": 4},
                                {"id": "fatima_sajtan", "name": "Fatima", "gen": 4},
                                {
                                    "id": "izet_sajtan", "name": "Izet", "gen": 4,
                                    "children": [
                                        {"id": "senada_izet_s", "name": "Senada", "gen": 5},
                                        {
                                            "id": "senad_izet_s", "name": "Senad", "gen": 5,
                                            "children": [
                                                {"id": "ajla_senad_s", "name": "Ajla", "gen": 6},
                                                {"id": "najla_senad_s", "name": "Najla", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": "muzijet_sajtan", "name": "Muzijet", "gen": 4,
                                    "children": [
                                        {
                                            "id": "almir_muzijet", "name": "Almir", "gen": 5,
                                            "children": [{"id": "anela_almir_m", "name": "Anela", "gen": 6}]
                                        },
                                        {
                                            "id": "admir_muzijet", "name": "Admir", "gen": 5,
                                            "children": [
                                                {"id": "dalila_admir_m", "name": "Dalila", "gen": 6},
                                                {"id": "ilda_admir_m", "name": "Ilda", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "ibrahim_adem", "name": "Ibrahim", "gen": 3,
                            "spouse": {"name": "Rukija", "notes": "r. Brčko"},
                            "children": [
                                {
                                    "id": "pasaga_ibrahim", "name": "Pašaga", "gen": 4,
                                    "spouse": {"name": "Nesiba", "notes": "r. Bešići"},
                                    "children": [
                                        {
                                            "id": "ibrahim_pasaga", "name": "Ibrahim", "gen": 5,
                                            "spouse": {"name": "Mina", "notes": "r. T. Brdo"},
                                            "children": [
                                                {"id": "amira_ibrahim_p", "name": "Amira", "gen": 6},
                                                {"id": "bahira_ibrahim_p", "name": "Bahira", "gen": 6},
                                                {"id": "sahza_ibrahim_p", "name": "Šahza", "gen": 6}
                                            ]
                                        },
                                        {"id": "mina_pasaga", "name": "Mina", "gen": 5},
                                        {"id": "muniba_pasaga", "name": "Muniba", "gen": 5},
                                        {"id": "rukija_pasaga", "name": "Rukija", "gen": 5},
                                        {"id": "tima_pasaga", "name": "Tima", "gen": 5},
                                        {
                                            "id": "cido_pasaga", "name": "Ćido", "gen": 5,
                                            "spouse": {"name": "Ramiza", "notes": "Supruga"},
                                            "children": [
                                                {"id": "jasmina_cido", "name": "Jasmina", "gen": 6},
                                                {"id": "azemina_cido", "name": "Azemina", "gen": 6}
                                            ]
                                        },
                                        {
                                            "id": "halil_pasaga", "name": "Halil", "gen": 5,
                                            "spouse": {"name": "Mina", "notes": "Supruga"},
                                            "children": [
                                                {
                                                    "id": "nedzad_halil_p", "name": "Nedžad", "gen": 6,
                                                    "children": [
                                                        {"id": "erna_nedzad_h", "name": "Erna", "gen": 7},
                                                        {"id": "lejla_nedzad_h", "name": "Lejla", "gen": 7}
                                                    ]
                                                },
                                                {
                                                    "id": "nesad_halil_p", "name": "Nešad", "gen": 6,
                                                    "children": [
                                                        {"id": "armina_nesad_h", "name": "Armina", "gen": 7},
                                                        {
                                                            "id": "armin_nesad_h", "name": "Armin", "gen": 7,
                                                            "children": [
                                                                {"id": "benjamin_armin_h", "name": "Benjamin", "gen": 8},
                                                                {"id": "adem_armin_h", "name": "Adem", "gen": 8}
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {"id": "adem_ibrahim_a", "name": "Adem", "notes": "n. Poginuo", "gen": 4},
                                {"id": "halil_ibrahim_a", "name": "Halil", "notes": "n. Poginuo", "gen": 4},
                                {"id": "zumra_ibrahim_a", "name": "Zumra", "gen": 4},
                                {"id": "sevka_ibrahim_a", "name": "Ševka", "gen": 4},
                                {"id": "izeta_ibrahim_a", "name": "Izeta", "gen": 4},
                                {"id": "zineta_ibrahim_a", "name": "Zineta", "gen": 4},
                                {
                                    "id": "atlaga_ibrahim_a", "name": "Atlaga", "gen": 4,
                                    "spouse": {"name": "Munira", "notes": "r. Bilalići"},
                                    "children": [
                                        {
                                            "id": "nuraga_atlaga", "name": "Nuraga", "gen": 5,
                                            "spouse": {"name": "Elvira", "notes": "Supruga"},
                                            "children": [
                                                {"id": "azra_nuraga", "name": "Azra", "gen": 6},
                                                {"id": "aida_nuraga", "name": "Aida", "gen": 6}
                                            ]
                                        },
                                        {"id": "kada_atlaga", "name": "Kada", "gen": 5},
                                        {"id": "suada_atlaga", "name": "Suada", "gen": 5},
                                        {
                                            "id": "adem_atlaga", "name": "Adem", "gen": 5,
                                            "spouse": {"name": "Velida", "notes": "Supruga"},
                                            "children": [
                                                {"id": "adisa_adem_at", "name": "Adisa", "gen": 6},
                                                {"id": "admir_adem_at", "name": "Admir", "gen": 6}
                                            ]
                                        },
                                        {
                                            "id": "beslaga_atlaga", "name": "Bešlaga", "gen": 5,
                                            "children": [
                                                {
                                                    "id": "edin_beslaga", "name": "Edin", "gen": 6,
                                                    "children": [
                                                        {"id": "sumeja_edin_b", "name": "Sumeja", "gen": 7},
                                                        {"id": "harun_edin_b", "name": "Harun", "gen": 7}
                                                    ]
                                                },
                                                {"id": "enver_beslaga", "name": "Enver", "gen": 6},
                                                {"id": "ismail_beslaga", "name": "Ismail", "gen": 6},
                                                {"id": "amina_beslaga", "name": "Amina", "gen": 6},
                                                {"id": "omer_beslaga", "name": "Omer", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "branch_name": "Branche Meho",
                "branch_color": "amber", # Ocre / Ambre doré
                "id": "meho_branch",
                "person": {
                    "id": "meho_1",
                    "name": "Meho",
                    "dates": "1867 – 1941",
                    "gen": 2,
                    "spouse": {"name": "Cura", "notes": "Supruga"},
                    "children": [
                        {
                            "id": "mehmed_meho", "name": "Mehmed", "dates": "1903 – 1945", "gen": 3,
                            "children": [
                                {
                                    "id": "bijader_mehmed_m", "name": "Bijader", "gen": 4,
                                    "spouse": {"name": "Zumreta", "notes": "Supruga"},
                                    "children": [
                                        {"id": "mensura_bijader", "name": "Mensura", "gen": 5},
                                        {"id": "mirsad_bijader", "name": "Mirsad", "gen": 5},
                                        {
                                            "id": "mehmed_bijader", "name": "Mehmed", "gen": 5,
                                            "spouse": {"name": "Zumra", "notes": "Supruga"},
                                            "children": [
                                                {"id": "meliha_mehmed_b", "name": "Meliha", "gen": 6},
                                                {"id": "emina_mehmed_b", "name": "Emina", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {"id": "velida_mehmed_m", "name": "Velida", "gen": 4},
                                {"id": "fadila_mehmed_m", "name": "Fadila", "gen": 4},
                                {"id": "velid_mehmed_m", "name": "Velid", "gen": 4},
                                {
                                    "id": "zedin_mehmed_m", "name": "Zedin", "gen": 4,
                                    "children": [
                                        {
                                            "id": "velid_zedin", "name": "Velid", "gen": 5,
                                            "spouse": {"name": "Marica", "notes": "Supruga"},
                                            "children": [
                                                {"id": "nenad_velid_z", "name": "Nenad", "gen": 6},
                                                {"id": "senad_velid_z", "name": "Senad", "gen": 6}
                                            ]
                                        },
                                        {"id": "zineta_zedin", "name": "Zineta", "gen": 5},
                                        {"id": "zehrija_zedin", "name": "Zehrija", "gen": 5},
                                        {
                                            "id": "zehrudin_zedin", "name": "Zehrudin", "gen": 5,
                                            "spouse": {"name": "Elvira", "notes": "Supruga"},
                                            "children": [
                                                {"id": "samira_zehrudin", "name": "Samira", "gen": 6},
                                                {"id": "alisa_zehrudin", "name": "Alisa", "gen": 6},
                                                {"id": "elvis_zehrudin", "name": "Elvis", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "sinan_meho", "name": "Sinan", "dates": "1907 – 1984", "gen": 3,
                            "spouse": {"name": "Aiša", "notes": "Supruga"},
                            "children": [
                                {
                                    "id": "asim_sinan", "name": "Asim", "gen": 4,
                                    "spouse": {"name": "Zorka", "notes": "Supruga"},
                                    "children": [{"id": "jasmina_asim", "name": "Jasmina", "gen": 5}]
                                },
                                {
                                    "id": "rasid_sinan", "name": "Rašid", "gen": 4,
                                    "spouse": {"name": "Kaima", "notes": "Supruga"},
                                    "children": [
                                        {"id": "lejla_rasid", "name": "Lejla", "gen": 5},
                                        {
                                            "id": "jasmin_rasid", "name": "Jasmin", "gen": 5,
                                            "children": [
                                                {"id": "kaima_jasmin_r", "name": "Kaima", "gen": 6},
                                                {"id": "kemal_jasmin_r", "name": "Kemal", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": "ahmo_sinan", "name": "Ahmo", "gen": 4,
                                    "spouse": {"name": "Hiba", "notes": "Supruga"},
                                    "children": [
                                        {"id": "hida_ahmo", "name": "Hida", "gen": 5},
                                        {
                                            "id": "nijaz_ahmo", "name": "Nijaz", "gen": 5,
                                            "spouse": {"name": "Arifa", "notes": "Supruga"},
                                            "children": [{"id": "ervin_nijaz_a", "name": "Ervin", "gen": 6}]
                                        }
                                    ]
                                },
                                {"id": "safa_sinan", "name": "Safa", "gen": 4},
                                {
                                    "id": "esad_sinan", "name": "Esad", "gen": 4,
                                    "spouse": {"name": "Nesiba", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "safet_esad", "name": "Safet", "gen": 5,
                                            "spouse": {"name": "Maida", "notes": "Supruga"},
                                            "children": [
                                                {"id": "sabina_safet", "name": "Sabina", "gen": 6},
                                                {"id": "emir_safet", "name": "Emir", "gen": 6},
                                                {"id": "semir_safet", "name": "Semir", "gen": 6}
                                            ]
                                        },
                                        {
                                            "id": "ahmet_esad", "name": "Ahmet", "gen": 5,
                                            "spouse": {"name": "Mejrema", "notes": "Supruga"},
                                            "children": [
                                                {"id": "mirsad_ahmet", "name": "Mirsad", "gen": 6},
                                                {"id": "mensur_ahmet", "name": "Mensur", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {"id": "mejra_meho", "name": "Mejra", "gen": 3},
                        {
                            "id": "huso_meho", "name": "Huso", "dates": "1913 – 1998", "gen": 3,
                            "spouse": {"name": "Hanka", "notes": "Supruga"},
                            "children": [
                                {"id": "pasa_huso", "name": "Paša", "gen": 4},
                                {"id": "nura_huso", "name": "Nura", "gen": 4},
                                {"id": "zemina_huso", "name": "Zemina", "gen": 4},
                                {
                                    "id": "mehan_huso", "name": "Mehan", "gen": 4,
                                    "spouse": {"name": "Fadila", "notes": "Supruga"},
                                    "children": [
                                        {"id": "mevlida_mehan", "name": "Mevlida", "gen": 5},
                                        {"id": "eldina_mehan", "name": "Eldina", "gen": 5},
                                        {
                                            "id": "mensur_mehan", "name": "Mensur", "gen": 5,
                                            "spouse": {"name": "Nermina", "notes": "Supruga"},
                                            "children": [
                                                {"id": "ajla_mensur_m", "name": "Ajla", "gen": 6},
                                                {"id": "lejla_mensur_m", "name": "Lejla", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "branch_name": "Branche Osman",
                "branch_color": "sky", # Bleu Ciel / Saphir doux
                "id": "osman_branch",
                "person": {
                    "id": "osman_1",
                    "name": "Osman",
                    "dates": "1860 – 1937",
                    "gen": 2,
                    "spouse": {"name": "Hata", "notes": "Supruga"},
                    "children": [
                        {"id": "fatima_osman_luke", "name": "Fatima", "notes": "u. Luke", "gen": 3},
                        {
                            "id": "avdo_osman", "name": "Avdo", "dates": "1887 – 1942", "gen": 3,
                            "spouse": {"name": "Mejra", "notes": "Supruga"},
                            "children": [
                                {
                                    "id": "sukrija_avdo_o", "name": "Šukrija", "gen": 4,
                                    "spouse": {"name": "Fehma", "notes": "Supruga"},
                                    "children": [
                                        {"id": "azra_sukrija", "name": "Azra", "gen": 5},
                                        {
                                            "id": "nijaz_sukrija", "name": "Nijaz", "gen": 5,
                                            "children": [
                                                {"id": "alen_nijaz_s", "name": "Alen", "gen": 6},
                                                {"id": "admir_nijaz_s", "name": "Admir", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {"id": "mehmed_avdo_o", "name": "Mehmed", "notes": "n. Poginuo u saobraćajnoj nesreći", "gen": 4},
                                {
                                    "id": "omer_avdo_o", "name": "Omer", "gen": 4,
                                    "spouse": {"name": "Fatima", "notes": "Supruga"}
                                },
                                {
                                    "id": "salkan_avdo_o", "name": "Salkan", "gen": 4,
                                    "spouse": {"name": "Havka", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "zekerijah_salkan", "name": "Zekerijah", "gen": 5,
                                            "children": [
                                                {
                                                    "id": "mersudin_zekerijah", "name": "Mersudin", "gen": 6,
                                                    "children": [
                                                        {"id": "majda_mersudin", "name": "Majda", "gen": 7},
                                                        {"id": "adi_mersudin", "name": "Adi", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": "avdo_salkan", "name": "Avdo", "gen": 5,
                                            "children": [
                                                {"id": "aida_avdo_s", "name": "Aida", "gen": 6},
                                                {"id": "larisa_avdo_s", "name": "Larisa", "gen": 6},
                                                {
                                                    "id": "vahid_avdo_s", "name": "Vahid", "gen": 6,
                                                    "children": [
                                                        {"id": "alina_vahid", "name": "Alina", "gen": 7},
                                                        {"id": "ajla_vahid", "name": "Ajla", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        },
                                        {"id": "zekija_salkan", "name": "Zekija", "gen": 5},
                                        {
                                            "id": "sevludin_salkan", "name": "Sevludin", "gen": 5,
                                            "children": [
                                                {"id": "adisa_sevludin", "name": "Adisa", "gen": 6},
                                                {"id": "amela_sevludin", "name": "Amela", "gen": 6}
                                            ]
                                        },
                                        {"id": "enes_salkan", "name": "Enes", "gen": 5},
                                        {"id": "bego_salkan", "name": "Bego", "gen": 5},
                                        {"id": "mirsad_salkan", "name": "Mirsad", "gen": 5},
                                        {
                                            "id": "muhidin_salkan", "name": "Muhidin", "gen": 5,
                                            "children": [
                                                {"id": "sanela_muhidin", "name": "Sanela", "gen": 6},
                                                {"id": "jasmin_muhidin", "name": "Jasmin", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "sahbaz_osman", "name": "Šahbaz", "dates": "1910 – 1998", "gen": 3,
                            "spouse": {"name": "Emka", "notes": "Supruga"},
                            "children": [
                                {
                                    "id": "osman_sahbaz", "name": "Osman", "gen": 4,
                                    "spouse": {"name": "Nura", "notes": "Supruga"},
                                    "children": [
                                        {"id": "vaila_osman_s", "name": "Vaila", "gen": 5},
                                        {"id": "zekira_osman_s", "name": "Zekira", "gen": 5},
                                        {"id": "azra_osman_s", "name": "Azra", "gen": 5}
                                    ]
                                },
                                {
                                    "id": "sevko_sahbaz", "name": "Ševko", "gen": 4,
                                    "spouse": {"name": "Džemila", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "nermin_sevko", "name": "Nermin", "gen": 5,
                                            "children": [
                                                {"id": "benjamin_nermin_s", "name": "Benjamin", "gen": 6},
                                                {"id": "albin_nermin_s", "name": "Albin", "gen": 6}
                                            ]
                                        },
                                        {"id": "elvedina_sevko", "name": "Elvedina", "gen": 5},
                                        {
                                            "id": "elvedin_sevko", "name": "Elvedin", "gen": 5,
                                            "children": [
                                                {"id": "emrah_elvedin", "name": "Emrah", "gen": 6},
                                                {"id": "amel_elvedin", "name": "Amel", "gen": 6},
                                                {"id": "emina_elvedin", "name": "Emina", "gen": 6},
                                                {"id": "adina_elvedin", "name": "Adina", "gen": 6}
                                            ]
                                        }
                                    ]
                                },
                                {"id": "sefika_sahbaz", "name": "Šefika", "gen": 4},
                                {"id": "mina_sahbaz", "name": "Mina", "gen": 4},
                                {
                                    "id": "ohro_sahbaz", "name": "Ohro", "gen": 4,
                                    "spouse": {"name": "Nizama", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "dzevad_ohro", "name": "Dževad", "gen": 5,
                                            "children": [
                                                {"id": "elma_dzevad_o", "name": "Elma", "gen": 6},
                                                {"id": "mirsad_dzevad_o", "name": "Mirsad", "gen": 6}
                                            ]
                                        },
                                        {
                                            "id": "nedzad_ohro", "name": "Nedžad", "gen": 5,
                                            "children": [
                                                {"id": "tarik_nedzad_o", "name": "Tarik", "gen": 6},
                                                {
                                                    "id": "arnis_nedzad_o", "name": "Arnis", "gen": 6,
                                                    "children": [{"id": "idriz_arnis", "name": "Idriz", "gen": 7}]
                                                },
                                                {
                                                    "id": "armin_nedzad_o", "name": "Armin", "gen": 6,
                                                    "children": [
                                                        {"id": "zejn_armin_o", "name": "Zejn", "gen": 7},
                                                        {"id": "hamza_armin_o", "name": "Hamza", "gen": 7},
                                                        {"id": "zekerijah_armin_o", "name": "Zekerijah", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "sacir_osman", "name": "Šaćir", "dates": "1914 – 1999", "gen": 3,
                            "spouse": {"name": "Alta", "notes": "Supruga"},
                            "children": [
                                {"id": "mevla_sacir", "name": "Mevla", "gen": 4},
                                {"id": "seida_sacir", "name": "Seida", "gen": 4},
                                {
                                    "id": "avdo_sacir", "name": "Avdo", "gen": 4,
                                    "spouse": {"name": "Izeta", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "izudin_avdo_sacir", "name": "Izudin", "gen": 5,
                                            "children": [
                                                {"id": "alma_izudin", "name": "Alma", "gen": 6},
                                                {"id": "amra_izudin", "name": "Amra", "gen": 6}
                                            ]
                                        },
                                        {
                                            "id": "mevludin_avdo_sacir", "name": "Mevludin", "gen": 5,
                                            "children": [
                                                {"id": "samra_mevludin", "name": "Samra", "gen": 6},
                                                {
                                                    "id": "asmir_mevludin", "name": "Asmir", "gen": 6,
                                                    "children": [{"id": "lejla_asmir_m", "name": "Lejla", "gen": 7}]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {"id": "azijada_sacir", "name": "Azijada", "gen": 4},
                                {
                                    "id": "omer_sacir", "name": "Omer", "gen": 4,
                                    "spouse": {"name": "Fatima", "notes": "Supruga"},
                                    "children": [
                                        {"id": "zekira_omer_sacir", "name": "Zekira", "gen": 5},
                                        {"id": "zehrina_omer_sacir", "name": "Zehrina", "gen": 5},
                                        {"id": "nermina_omer_sacir", "name": "Nermina", "gen": 5},
                                        {
                                            "id": "nermin_omer_sacir", "name": "Nermin", "gen": 5,
                                            "children": [
                                                {"id": "ajlin_nermin_os", "name": "Ajlin", "gen": 6},
                                                {"id": "davud_nermin_os", "name": "Davud", "gen": 6}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "muharem_osman", "name": "Muharem", "gen": 3,
                            "spouse": {"name": "Mejra", "notes": "Supruga"},
                            "children": [
                                {
                                    "id": "resid_muharem", "name": "Rešid", "gen": 4,
                                    "spouse": {"name": "Aiša", "notes": "Supruga"},
                                    "children": [
                                        {"id": "zikreta_resid", "name": "Zikreta", "gen": 5},
                                        {"id": "zekerijah_resid", "name": "Zekerijah", "gen": 5},
                                        {"id": "mensur_resid", "name": "Mensur", "gen": 5}
                                    ]
                                },
                                {
                                    "id": "rasim_muharem", "name": "Rasim", "gen": 4,
                                    "spouse": {"name": "Kadira", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "ramiz_rasim", "name": "Ramiz", "gen": 5,
                                            "children": [
                                                {"id": "selma_ramiz_poginula", "name": "Selma", "notes": "n. Poginula", "gen": 6},
                                                {
                                                    "id": "almir_ramiz", "name": "Almir", "gen": 6,
                                                    "children": [
                                                        {"id": "amra_almir_r", "name": "Amra", "gen": 7},
                                                        {"id": "adna_almir_r", "name": "Adna", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        },
                                        {"id": "hanifa_rasim", "name": "Hanifa", "gen": 5},
                                        {"id": "dzemila_rasim", "name": "Džemila", "gen": 5},
                                        {
                                            "id": "rizvo_rasim", "name": "Rizvo", "gen": 5,
                                            "children": [
                                                {"id": "sanela_rizvo", "name": "Sanela", "gen": 6},
                                                {"id": "admira_rizvo", "name": "Admira", "gen": 6},
                                                {
                                                    "id": "admir_rizvo", "name": "Admir", "gen": 6,
                                                    "children": [
                                                        {"id": "armina_admir_r", "name": "Armina", "gen": 7},
                                                        {"id": "amina_admir_r", "name": "Amina", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": "irfan_rasim", "name": "Irfan", "gen": 5,
                                            "children": [
                                                {"id": "sabina_irfan", "name": "Sabina", "gen": 6},
                                                {"id": "jasmina_irfan", "name": "Jasmina", "gen": 6},
                                                {
                                                    "id": "jasmin_irfan", "name": "Jasmin", "gen": 6,
                                                    "children": [
                                                        {"id": "konstantin_jasmin_i", "name": "Konstantin", "gen": 7},
                                                        {"id": "viktor_jasmin_i", "name": "Viktor", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {"id": "hanka_muharem", "name": "Hanka", "gen": 4},
                                {"id": "malka_muharem", "name": "Malka", "gen": 4},
                                {"id": "tifa_muharem", "name": "Tifa", "gen": 4},
                                {
                                    "id": "mehmedalija_muharem", "name": "Mehmedalija", "gen": 4,
                                    "spouse": {"name": "Rajfa", "notes": "Supruga"},
                                    "children": [
                                        {
                                            "id": "seudin_mehmedalija", "name": "Seudin", "gen": 5,
                                            "children": [
                                                {
                                                    "id": "suvad_seudin", "name": "Suvad", "gen": 6,
                                                    "children": [
                                                        {"id": "sara_suvad", "name": "Sara", "gen": 7},
                                                        {"id": "malik_suvad", "name": "Malik", "gen": 7}
                                                    ]
                                                },
                                                {"id": "dzevida_seudin", "name": "Dževida", "gen": 6},
                                                {
                                                    "id": "dzevad_seudin", "name": "Dževad", "gen": 6,
                                                    "children": [
                                                        {"id": "eldin_dzevad_s", "name": "Eldin", "gen": 7},
                                                        {"id": "anel_dzevad_s", "name": "Anel", "gen": 7},
                                                        {"id": "elma_dzevad_s", "name": "Elma", "gen": 7}
                                                    ]
                                                }
                                            ]
                                        },
                                        {"id": "remza_mehmedalija", "name": "Remza", "gen": 5},
                                        {
                                            "id": "jusuf_mehmedalija", "name": "Jusuf", "gen": 5,
                                            "children": [
                                                {"id": "emina_jusuf", "name": "Emina", "gen": 6},
                                                {"id": "mehmedalija_jusuf", "name": "Mehmedalija", "gen": 6},
                                                {"id": "amir_jusuf", "name": "Amir", "gen": 6},
                                                {"id": "amra_jusuf", "name": "Amra", "gen": 6},
                                                {"id": "almedina_jusuf", "name": "Almedina", "gen": 6},
                                                {"id": "senad_jusuf", "name": "Senad", "gen": 6}
                                            ]
                                        },
                                        {"id": "nasiha_mehmedalija", "name": "Nasiha", "gen": 5},
                                        {
                                            "id": "sefik_mehmedalija", "name": "Šefik", "gen": 5,
                                            "children": [
                                                {"id": "edina_sefik_m", "name": "Edina", "gen": 6},
                                                {
                                                    "id": "edin_sefik_m", "name": "Edin", "gen": 6,
                                                    "spouse": {"name": "Mubina", "notes": "Supruga"},
                                                    "children": [
                                                        {"id": "dzenana_edin_s", "name": "Dženana", "gen": 7},
                                                        {"id": "mirsad_edin_s", "name": "Mirsad", "gen": 7},
                                                        {"id": "elmir_edin_s", "name": "Elmir", "gen": 7},
                                                        {"id": "elma_edin_s", "name": "Elma", "gen": 7},
                                                        {
                                                            "id": "adis_edin_s", "name": "Adis", "gen": 7,
                                                            "children": [{"id": "maja_adis", "name": "Maja", "gen": 8}]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "branch_name": "Branche Nurif",
                "branch_color": "rose", # Rose poudré / Pêche
                "id": "nurif_branch",
                "person": {
                    "id": "nurif_1",
                    "name": "Nurif",
                    "dates": "r. 1863",
                    "notes": "",
                    "gen": 2,
                    "children": []
                }
            },
            {
                "branch_name": "Branche Paša",
                "branch_color": "violet", # Lavande / Prune douce
                "id": "pasa_branch",
                "person": {
                    "id": "pasa_1",
                    "name": "Paša",
                    "dates": "",
                    "notes": "u. Glinje, u. Hrustanović",
                    "gen": 2,
                    "children": []
                }
            }
        ]
    }
}

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(tree_data, f, ensure_ascii=False, indent=2)

print("Saved family_tree_structured.json")
