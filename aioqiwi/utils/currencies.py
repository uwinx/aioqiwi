from dataclasses import dataclass


@dataclass
class Currency:
    code: str
    decimal_digits: int
    name: str
    name_plural: str
    rounding: int
    symbol: str
    symbol_native: str


codes_number = {
    "008": "ALL",
    "012": "DZD",
    "032": "ARS",
    "036": "AUD",
    "044": "BSD",
    "048": "BHD",
    "050": "BDT",
    "051": "AMD",
    "052": "BBD",
    "060": "BMD",
    "064": "BTN",
    "068": "BOB",
    "072": "BWP",
    "084": "BZD",
    "090": "SBD",
    "096": "BND",
    "104": "MMK",
    "108": "BIF",
    "116": "KHR",
    "124": "CAD",
    "132": "CVE",
    "136": "KYD",
    "144": "LKR",
    "152": "CLP",
    "156": "CNY",
    "170": "COP",
    "174": "KMF",
    "188": "CRC",
    "191": "HRK",
    "192": "CUP",
    "203": "CZK",
    "208": "DKK",
    "214": "DOP",
    "222": "SVC",
    "230": "ETB",
    "232": "ERN",
    "238": "FKP",
    "242": "FJD",
    "262": "DJF",
    "270": "GMD",
    "292": "GIP",
    "320": "GTQ",
    "324": "GNF",
    "328": "GYD",
    "332": "HTG",
    "340": "HNL",
    "344": "HKD",
    "348": "HUF",
    "352": "ISK",
    "356": "INR",
    "360": "IDR",
    "364": "IRR",
    "368": "IQD",
    "376": "ILS",
    "388": "JMD",
    "392": "JPY",
    "398": "KZT",
    "400": "JOD",
    "404": "KES",
    "408": "KPW",
    "410": "KRW",
    "414": "KWD",
    "417": "KGS",
    "418": "LAK",
    "422": "LBP",
    "426": "LSL",
    "430": "LRD",
    "434": "LYD",
    "446": "MOP",
    "454": "MWK",
    "458": "MYR",
    "462": "MVR",
    "480": "MUR",
    "484": "MXN",
    "496": "MNT",
    "498": "MDL",
    "504": "MAD",
    "512": "OMR",
    "516": "NAD",
    "524": "NPR",
    "532": "ANG",
    "533": "AWG",
    "548": "VUV",
    "554": "NZD",
    "558": "NIO",
    "566": "NGN",
    "578": "NOK",
    "586": "PKR",
    "590": "PAB",
    "598": "PGK",
    "600": "PYG",
    "604": "PEN",
    "608": "PHP",
    "634": "QAR",
    "643": "RUB",
    "646": "RWF",
    "654": "SHP",
    "682": "SAR",
    "690": "SCR",
    "694": "SLL",
    "702": "SGD",
    "704": "VND",
    "706": "SOS",
    "710": "ZAR",
    "728": "SSP",
    "748": "SZL",
    "752": "SEK",
    "756": "CHF",
    "760": "SYP",
    "764": "THB",
    "776": "TOP",
    "780": "TTD",
    "784": "AED",
    "788": "TND",
    "800": "UGX",
    "807": "MKD",
    "818": "EGP",
    "826": "GBP",
    "834": "TZS",
    "840": "USD",
    "858": "UYU",
    "860": "UZS",
    "882": "WST",
    "886": "YER",
    "901": "TWD",
    "929": "MRU",
    "930": "STN",
    "931": "CUC",
    "932": "ZWL",
    "934": "TMT",
    "936": "GHS",
    "937": "VEF",
    "938": "SDG",
    "940": "UYI",
    "941": "RSD",
    "943": "MZN",
    "944": "AZN",
    "946": "RON",
    "947": "CHE",
    "948": "CHW",
    "949": "TRY",
    "950": "XAF",
    "951": "XCD",
    "952": "XOF",
    "953": "XPF",
    "960": "XDR",
    "965": "XUA",
    "967": "ZMW",
    "968": "SRD",
    "969": "MGA",
    "970": "COU",
    "971": "AFN",
    "972": "TJS",
    "973": "AOA",
    "974": "BYR",
    "975": "BGN",
    "976": "CDF",
    "977": "BAM",
    "978": "EUR",
    "979": "MXV",
    "980": "UAH",
    "981": "GEL",
    "984": "BOV",
    "985": "PLN",
    "986": "BRL",
    "990": "CLF",
    "994": "XSU",
    "997": "USN",
}

described = {
    "USD": Currency(
        **{
            "symbol": "$",
            "name": "US Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "USD",
            "name_plural": "US dollars",
        }
    ),
    "CAD": Currency(
        **{
            "symbol": "CA$",
            "name": "Canadian Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CAD",
            "name_plural": "Canadian dollars",
        }
    ),
    "EUR": Currency(
        **{
            "symbol": "€",
            "name": "Euro",
            "symbol_native": "€",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "EUR",
            "name_plural": "euros",
        }
    ),
    "AED": Currency(
        **{
            "symbol": "AED",
            "name": "United Arab Emirates Dirham",
            "symbol_native": "د.إ.\u200f",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "AED",
            "name_plural": "UAE dirhams",
        }
    ),
    "AFN": Currency(
        **{
            "symbol": "Af",
            "name": "Afghan Afghani",
            "symbol_native": "؋",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "AFN",
            "name_plural": "Afghan Afghanis",
        }
    ),
    "ALL": Currency(
        **{
            "symbol": "ALL",
            "name": "Albanian Lek",
            "symbol_native": "Lek",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "ALL",
            "name_plural": "Albanian lekë",
        }
    ),
    "AMD": Currency(
        **{
            "symbol": "AMD",
            "name": "Armenian Dram",
            "symbol_native": "դր.",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "AMD",
            "name_plural": "Armenian drams",
        }
    ),
    "ARS": Currency(
        **{
            "symbol": "AR$",
            "name": "Argentine Peso",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "ARS",
            "name_plural": "Argentine pesos",
        }
    ),
    "AUD": Currency(
        **{
            "symbol": "AU$",
            "name": "Australian Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "AUD",
            "name_plural": "Australian dollars",
        }
    ),
    "AZN": Currency(
        **{
            "symbol": "man.",
            "name": "Azerbaijani Manat",
            "symbol_native": "ман.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "AZN",
            "name_plural": "Azerbaijani manats",
        }
    ),
    "BAM": Currency(
        **{
            "symbol": "KM",
            "name": "Bosnia-Herzegovina Convertible Mark",
            "symbol_native": "KM",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BAM",
            "name_plural": "Bosnia-Herzegovina convertible marks",
        }
    ),
    "BDT": Currency(
        **{
            "symbol": "Tk",
            "name": "Bangladeshi Taka",
            "symbol_native": "৳",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BDT",
            "name_plural": "Bangladeshi takas",
        }
    ),
    "BGN": Currency(
        **{
            "symbol": "BGN",
            "name": "Bulgarian Lev",
            "symbol_native": "лв.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BGN",
            "name_plural": "Bulgarian leva",
        }
    ),
    "BHD": Currency(
        **{
            "symbol": "BD",
            "name": "Bahraini Dinar",
            "symbol_native": "د.ب.\u200f",
            "decimal_digits": 3,
            "rounding": 0,
            "code": "BHD",
            "name_plural": "Bahraini dinars",
        }
    ),
    "BIF": Currency(
        **{
            "symbol": "FBu",
            "name": "Burundian Franc",
            "symbol_native": "FBu",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "BIF",
            "name_plural": "Burundian francs",
        }
    ),
    "BND": Currency(
        **{
            "symbol": "BN$",
            "name": "Brunei Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BND",
            "name_plural": "Brunei dollars",
        }
    ),
    "BOB": Currency(
        **{
            "symbol": "Bs",
            "name": "Bolivian Boliviano",
            "symbol_native": "Bs",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BOB",
            "name_plural": "Bolivian bolivianos",
        }
    ),
    "BRL": Currency(
        **{
            "symbol": "R$",
            "name": "Brazilian Real",
            "symbol_native": "R$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BRL",
            "name_plural": "Brazilian reals",
        }
    ),
    "BWP": Currency(
        **{
            "symbol": "BWP",
            "name": "Botswanan Pula",
            "symbol_native": "P",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BWP",
            "name_plural": "Botswanan pulas",
        }
    ),
    "BYR": Currency(
        **{
            "symbol": "BYR",
            "name": "Belarusian Ruble",
            "symbol_native": "BYR",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "BYR",
            "name_plural": "Belarusian rubles",
        }
    ),
    "BZD": Currency(
        **{
            "symbol": "BZ$",
            "name": "Belize Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "BZD",
            "name_plural": "Belize dollars",
        }
    ),
    "CDF": Currency(
        **{
            "symbol": "CDF",
            "name": "Congolese Franc",
            "symbol_native": "FrCD",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CDF",
            "name_plural": "Congolese francs",
        }
    ),
    "CHF": Currency(
        **{
            "symbol": "CHF",
            "name": "Swiss Franc",
            "symbol_native": "CHF",
            "decimal_digits": 2,
            "rounding": 0.05,
            "code": "CHF",
            "name_plural": "Swiss francs",
        }
    ),
    "CLP": Currency(
        **{
            "symbol": "CL$",
            "name": "Chilean Peso",
            "symbol_native": "$",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "CLP",
            "name_plural": "Chilean pesos",
        }
    ),
    "CNY": Currency(
        **{
            "symbol": "CN¥",
            "name": "Chinese Yuan",
            "symbol_native": "CN¥",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CNY",
            "name_plural": "Chinese yuan",
        }
    ),
    "COP": Currency(
        **{
            "symbol": "CO$",
            "name": "Colombian Peso",
            "symbol_native": "$",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "COP",
            "name_plural": "Colombian pesos",
        }
    ),
    "CRC": Currency(
        **{
            "symbol": "₡",
            "name": "Costa Rican Colón",
            "symbol_native": "₡",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "CRC",
            "name_plural": "Costa Rican colóns",
        }
    ),
    "CVE": Currency(
        **{
            "symbol": "CV$",
            "name": "Cape Verdean Escudo",
            "symbol_native": "CV$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CVE",
            "name_plural": "Cape Verdean escudos",
        }
    ),
    "CZK": Currency(
        **{
            "symbol": "Kč",
            "name": "Czech Republic Koruna",
            "symbol_native": "Kč",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CZK",
            "name_plural": "Czech Republic korunas",
        }
    ),
    "DJF": Currency(
        **{
            "symbol": "Fdj",
            "name": "Djiboutian Franc",
            "symbol_native": "Fdj",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "DJF",
            "name_plural": "Djiboutian francs",
        }
    ),
    "DKK": Currency(
        **{
            "symbol": "Dkr",
            "name": "Danish Krone",
            "symbol_native": "kr",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "DKK",
            "name_plural": "Danish kroner",
        }
    ),
    "DOP": Currency(
        **{
            "symbol": "RD$",
            "name": "Dominican Peso",
            "symbol_native": "RD$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "DOP",
            "name_plural": "Dominican pesos",
        }
    ),
    "DZD": Currency(
        **{
            "symbol": "DA",
            "name": "Algerian Dinar",
            "symbol_native": "د.ج.\u200f",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "DZD",
            "name_plural": "Algerian dinars",
        }
    ),
    "EEK": Currency(
        **{
            "symbol": "Ekr",
            "name": "Estonian Kroon",
            "symbol_native": "kr",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "EEK",
            "name_plural": "Estonian kroons",
        }
    ),
    "EGP": Currency(
        **{
            "symbol": "EGP",
            "name": "Egyptian Pound",
            "symbol_native": "ج.م.\u200f",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "EGP",
            "name_plural": "Egyptian pounds",
        }
    ),
    "ERN": Currency(
        **{
            "symbol": "Nfk",
            "name": "Eritrean Nakfa",
            "symbol_native": "Nfk",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "ERN",
            "name_plural": "Eritrean nakfas",
        }
    ),
    "ETB": Currency(
        **{
            "symbol": "Br",
            "name": "Ethiopian Birr",
            "symbol_native": "Br",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "ETB",
            "name_plural": "Ethiopian birrs",
        }
    ),
    "GBP": Currency(
        **{
            "symbol": "£",
            "name": "British Pound Sterling",
            "symbol_native": "£",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "GBP",
            "name_plural": "British pounds sterling",
        }
    ),
    "GEL": Currency(
        **{
            "symbol": "GEL",
            "name": "Georgian Lari",
            "symbol_native": "GEL",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "GEL",
            "name_plural": "Georgian laris",
        }
    ),
    "GHS": Currency(
        **{
            "symbol": "GH₵",
            "name": "Ghanaian Cedi",
            "symbol_native": "GH₵",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "GHS",
            "name_plural": "Ghanaian cedis",
        }
    ),
    "GNF": Currency(
        **{
            "symbol": "FG",
            "name": "Guinean Franc",
            "symbol_native": "FG",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "GNF",
            "name_plural": "Guinean francs",
        }
    ),
    "GTQ": Currency(
        **{
            "symbol": "GTQ",
            "name": "Guatemalan Quetzal",
            "symbol_native": "Q",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "GTQ",
            "name_plural": "Guatemalan quetzals",
        }
    ),
    "HKD": Currency(
        **{
            "symbol": "HK$",
            "name": "Hong Kong Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "HKD",
            "name_plural": "Hong Kong dollars",
        }
    ),
    "HNL": Currency(
        **{
            "symbol": "HNL",
            "name": "Honduran Lempira",
            "symbol_native": "L",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "HNL",
            "name_plural": "Honduran lempiras",
        }
    ),
    "HRK": Currency(
        **{
            "symbol": "kn",
            "name": "Croatian Kuna",
            "symbol_native": "kn",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "HRK",
            "name_plural": "Croatian kunas",
        }
    ),
    "HUF": Currency(
        **{
            "symbol": "Ft",
            "name": "Hungarian Forint",
            "symbol_native": "Ft",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "HUF",
            "name_plural": "Hungarian forints",
        }
    ),
    "IDR": Currency(
        **{
            "symbol": "Rp",
            "name": "Indonesian Rupiah",
            "symbol_native": "Rp",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "IDR",
            "name_plural": "Indonesian rupiahs",
        }
    ),
    "ILS": Currency(
        **{
            "symbol": "₪",
            "name": "Israeli New Sheqel",
            "symbol_native": "₪",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "ILS",
            "name_plural": "Israeli new sheqels",
        }
    ),
    "INR": Currency(
        **{
            "symbol": "Rs",
            "name": "Indian Rupee",
            "symbol_native": "টকা",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "INR",
            "name_plural": "Indian rupees",
        }
    ),
    "IQD": Currency(
        **{
            "symbol": "IQD",
            "name": "Iraqi Dinar",
            "symbol_native": "د.ع.\u200f",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "IQD",
            "name_plural": "Iraqi dinars",
        }
    ),
    "IRR": Currency(
        **{
            "symbol": "IRR",
            "name": "Iranian Rial",
            "symbol_native": "﷼",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "IRR",
            "name_plural": "Iranian rials",
        }
    ),
    "ISK": Currency(
        **{
            "symbol": "Ikr",
            "name": "Icelandic Króna",
            "symbol_native": "kr",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "ISK",
            "name_plural": "Icelandic krónur",
        }
    ),
    "JMD": Currency(
        **{
            "symbol": "J$",
            "name": "Jamaican Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "JMD",
            "name_plural": "Jamaican dollars",
        }
    ),
    "JOD": Currency(
        **{
            "symbol": "JD",
            "name": "Jordanian Dinar",
            "symbol_native": "د.أ.\u200f",
            "decimal_digits": 3,
            "rounding": 0,
            "code": "JOD",
            "name_plural": "Jordanian dinars",
        }
    ),
    "JPY": Currency(
        **{
            "symbol": "¥",
            "name": "Japanese Yen",
            "symbol_native": "￥",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "JPY",
            "name_plural": "Japanese yen",
        }
    ),
    "KES": Currency(
        **{
            "symbol": "Ksh",
            "name": "Kenyan Shilling",
            "symbol_native": "Ksh",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KES",
            "name_plural": "Kenyan shillings",
        }
    ),
    "KHR": Currency(
        **{
            "symbol": "KHR",
            "name": "Cambodian Riel",
            "symbol_native": "៛",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KHR",
            "name_plural": "Cambodian riels",
        }
    ),
    "KMF": Currency(
        **{
            "symbol": "CF",
            "name": "Comorian Franc",
            "symbol_native": "FC",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "KMF",
            "name_plural": "Comorian francs",
        }
    ),
    "KRW": Currency(
        **{
            "symbol": "₩",
            "name": "South Korean Won",
            "symbol_native": "₩",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "KRW",
            "name_plural": "South Korean won",
        }
    ),
    "KWD": Currency(
        **{
            "symbol": "KD",
            "name": "Kuwaiti Dinar",
            "symbol_native": "د.ك.\u200f",
            "decimal_digits": 3,
            "rounding": 0,
            "code": "KWD",
            "name_plural": "Kuwaiti dinars",
        }
    ),
    "KZT": Currency(
        **{
            "symbol": "KZT",
            "name": "Kazakhstani Tenge",
            "symbol_native": "тңг.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KZT",
            "name_plural": "Kazakhstani tenges",
        }
    ),
    "LBP": Currency(
        **{
            "symbol": "LB£",
            "name": "Lebanese Pound",
            "symbol_native": "ل.ل.\u200f",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "LBP",
            "name_plural": "Lebanese pounds",
        }
    ),
    "LKR": Currency(
        **{
            "symbol": "SLRs",
            "name": "Sri Lankan Rupee",
            "symbol_native": "SL Re",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "LKR",
            "name_plural": "Sri Lankan rupees",
        }
    ),
    "LTL": Currency(
        **{
            "symbol": "Lt",
            "name": "Lithuanian Litas",
            "symbol_native": "Lt",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "LTL",
            "name_plural": "Lithuanian litai",
        }
    ),
    "LVL": Currency(
        **{
            "symbol": "Ls",
            "name": "Latvian Lats",
            "symbol_native": "Ls",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "LVL",
            "name_plural": "Latvian lati",
        }
    ),
    "LYD": Currency(
        **{
            "symbol": "LD",
            "name": "Libyan Dinar",
            "symbol_native": "د.ل.\u200f",
            "decimal_digits": 3,
            "rounding": 0,
            "code": "LYD",
            "name_plural": "Libyan dinars",
        }
    ),
    "MAD": Currency(
        **{
            "symbol": "MAD",
            "name": "Moroccan Dirham",
            "symbol_native": "د.م.\u200f",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MAD",
            "name_plural": "Moroccan dirhams",
        }
    ),
    "MDL": Currency(
        **{
            "symbol": "MDL",
            "name": "Moldovan Leu",
            "symbol_native": "MDL",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MDL",
            "name_plural": "Moldovan lei",
        }
    ),
    "MGA": Currency(
        **{
            "symbol": "MGA",
            "name": "Malagasy Ariary",
            "symbol_native": "MGA",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "MGA",
            "name_plural": "Malagasy Ariaries",
        }
    ),
    "MKD": Currency(
        **{
            "symbol": "MKD",
            "name": "Macedonian Denar",
            "symbol_native": "MKD",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MKD",
            "name_plural": "Macedonian denari",
        }
    ),
    "MMK": Currency(
        **{
            "symbol": "MMK",
            "name": "Myanma Kyat",
            "symbol_native": "K",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "MMK",
            "name_plural": "Myanma kyats",
        }
    ),
    "MOP": Currency(
        **{
            "symbol": "MOP$",
            "name": "Macanese Pataca",
            "symbol_native": "MOP$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MOP",
            "name_plural": "Macanese patacas",
        }
    ),
    "MUR": Currency(
        **{
            "symbol": "MURs",
            "name": "Mauritian Rupee",
            "symbol_native": "MURs",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "MUR",
            "name_plural": "Mauritian rupees",
        }
    ),
    "MXN": Currency(
        **{
            "symbol": "MX$",
            "name": "Mexican Peso",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MXN",
            "name_plural": "Mexican pesos",
        }
    ),
    "MYR": Currency(
        **{
            "symbol": "RM",
            "name": "Malaysian Ringgit",
            "symbol_native": "RM",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MYR",
            "name_plural": "Malaysian ringgits",
        }
    ),
    "MZN": Currency(
        **{
            "symbol": "MTn",
            "name": "Mozambican Metical",
            "symbol_native": "MTn",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "MZN",
            "name_plural": "Mozambican meticals",
        }
    ),
    "NAD": Currency(
        **{
            "symbol": "N$",
            "name": "Namibian Dollar",
            "symbol_native": "N$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "NAD",
            "name_plural": "Namibian dollars",
        }
    ),
    "NGN": Currency(
        **{
            "symbol": "₦",
            "name": "Nigerian Naira",
            "symbol_native": "₦",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "NGN",
            "name_plural": "Nigerian nairas",
        }
    ),
    "NIO": Currency(
        **{
            "symbol": "C$",
            "name": "Nicaraguan Córdoba",
            "symbol_native": "C$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "NIO",
            "name_plural": "Nicaraguan córdobas",
        }
    ),
    "NOK": Currency(
        **{
            "symbol": "Nkr",
            "name": "Norwegian Krone",
            "symbol_native": "kr",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "NOK",
            "name_plural": "Norwegian kroner",
        }
    ),
    "NPR": Currency(
        **{
            "symbol": "NPRs",
            "name": "Nepalese Rupee",
            "symbol_native": "नेरू",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "NPR",
            "name_plural": "Nepalese rupees",
        }
    ),
    "NZD": Currency(
        **{
            "symbol": "NZ$",
            "name": "New Zealand Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "NZD",
            "name_plural": "New Zealand dollars",
        }
    ),
    "OMR": Currency(
        **{
            "symbol": "OMR",
            "name": "Omani Rial",
            "symbol_native": "ر.ع.\u200f",
            "decimal_digits": 3,
            "rounding": 0,
            "code": "OMR",
            "name_plural": "Omani rials",
        }
    ),
    "PAB": Currency(
        **{
            "symbol": "B/.",
            "name": "Panamanian Balboa",
            "symbol_native": "B/.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "PAB",
            "name_plural": "Panamanian balboas",
        }
    ),
    "PEN": Currency(
        **{
            "symbol": "S/.",
            "name": "Peruvian Nuevo Sol",
            "symbol_native": "S/.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "PEN",
            "name_plural": "Peruvian nuevos soles",
        }
    ),
    "PHP": Currency(
        **{
            "symbol": "₱",
            "name": "Philippine Peso",
            "symbol_native": "₱",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "PHP",
            "name_plural": "Philippine pesos",
        }
    ),
    "PKR": Currency(
        **{
            "symbol": "PKRs",
            "name": "Pakistani Rupee",
            "symbol_native": "₨",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "PKR",
            "name_plural": "Pakistani rupees",
        }
    ),
    "PLN": Currency(
        **{
            "symbol": "zł",
            "name": "Polish Zloty",
            "symbol_native": "zł",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "PLN",
            "name_plural": "Polish zlotys",
        }
    ),
    "PYG": Currency(
        **{
            "symbol": "₲",
            "name": "Paraguayan Guarani",
            "symbol_native": "₲",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "PYG",
            "name_plural": "Paraguayan guaranis",
        }
    ),
    "QAR": Currency(
        **{
            "symbol": "QR",
            "name": "Qatari Rial",
            "symbol_native": "ر.ق.\u200f",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "QAR",
            "name_plural": "Qatari rials",
        }
    ),
    "RON": Currency(
        **{
            "symbol": "RON",
            "name": "Romanian Leu",
            "symbol_native": "RON",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "RON",
            "name_plural": "Romanian lei",
        }
    ),
    "RSD": Currency(
        **{
            "symbol": "din.",
            "name": "Serbian Dinar",
            "symbol_native": "дин.",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "RSD",
            "name_plural": "Serbian dinars",
        }
    ),
    "RUB": Currency(
        **{
            "symbol": "RUB",
            "name": "Russian Ruble",
            "symbol_native": "руб.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "RUB",
            "name_plural": "Russian rubles",
        }
    ),
    "RWF": Currency(
        **{
            "symbol": "RWF",
            "name": "Rwandan Franc",
            "symbol_native": "FR",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "RWF",
            "name_plural": "Rwandan francs",
        }
    ),
    "SAR": Currency(
        **{
            "symbol": "SR",
            "name": "Saudi Riyal",
            "symbol_native": "ر.س.\u200f",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "SAR",
            "name_plural": "Saudi riyals",
        }
    ),
    "SDG": Currency(
        **{
            "symbol": "SDG",
            "name": "Sudanese Pound",
            "symbol_native": "SDG",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "SDG",
            "name_plural": "Sudanese pounds",
        }
    ),
    "SEK": Currency(
        **{
            "symbol": "Skr",
            "name": "Swedish Krona",
            "symbol_native": "kr",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "SEK",
            "name_plural": "Swedish kronor",
        }
    ),
    "SGD": Currency(
        **{
            "symbol": "S$",
            "name": "Singapore Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "SGD",
            "name_plural": "Singapore dollars",
        }
    ),
    "SOS": Currency(
        **{
            "symbol": "Ssh",
            "name": "Somali Shilling",
            "symbol_native": "Ssh",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "SOS",
            "name_plural": "Somali shillings",
        }
    ),
    "SYP": Currency(
        **{
            "symbol": "SY£",
            "name": "Syrian Pound",
            "symbol_native": "ل.س.\u200f",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "SYP",
            "name_plural": "Syrian pounds",
        }
    ),
    "THB": Currency(
        **{
            "symbol": "฿",
            "name": "Thai Baht",
            "symbol_native": "฿",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "THB",
            "name_plural": "Thai baht",
        }
    ),
    "TND": Currency(
        **{
            "symbol": "DT",
            "name": "Tunisian Dinar",
            "symbol_native": "د.ت.\u200f",
            "decimal_digits": 3,
            "rounding": 0,
            "code": "TND",
            "name_plural": "Tunisian dinars",
        }
    ),
    "TOP": Currency(
        **{
            "symbol": "T$",
            "name": "Tongan Paʻanga",
            "symbol_native": "T$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "TOP",
            "name_plural": "Tongan paʻanga",
        }
    ),
    "TRY": Currency(
        **{
            "symbol": "TL",
            "name": "Turkish Lira",
            "symbol_native": "TL",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "TRY",
            "name_plural": "Turkish Lira",
        }
    ),
    "TTD": Currency(
        **{
            "symbol": "TT$",
            "name": "Trinidad and Tobago Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "TTD",
            "name_plural": "Trinidad and Tobago dollars",
        }
    ),
    "TWD": Currency(
        **{
            "symbol": "NT$",
            "name": "New Taiwan Dollar",
            "symbol_native": "NT$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "TWD",
            "name_plural": "New Taiwan dollars",
        }
    ),
    "TZS": Currency(
        **{
            "symbol": "TSh",
            "name": "Tanzanian Shilling",
            "symbol_native": "TSh",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "TZS",
            "name_plural": "Tanzanian shillings",
        }
    ),
    "UAH": Currency(
        **{
            "symbol": "₴",
            "name": "Ukrainian Hryvnia",
            "symbol_native": "₴",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "UAH",
            "name_plural": "Ukrainian hryvnias",
        }
    ),
    "UGX": Currency(
        **{
            "symbol": "USh",
            "name": "Ugandan Shilling",
            "symbol_native": "USh",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "UGX",
            "name_plural": "Ugandan shillings",
        }
    ),
    "UYU": Currency(
        **{
            "symbol": "$U",
            "name": "Uruguayan Peso",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "UYU",
            "name_plural": "Uruguayan pesos",
        }
    ),
    "UZS": Currency(
        **{
            "symbol": "UZS",
            "name": "Uzbekistan Som",
            "symbol_native": "UZS",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "UZS",
            "name_plural": "Uzbekistan som",
        }
    ),
    "VEF": Currency(
        **{
            "symbol": "Bs.F.",
            "name": "Venezuelan Bolívar",
            "symbol_native": "Bs.F.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "VEF",
            "name_plural": "Venezuelan bolívars",
        }
    ),
    "VND": Currency(
        **{
            "symbol": "₫",
            "name": "Vietnamese Dong",
            "symbol_native": "₫",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "VND",
            "name_plural": "Vietnamese dong",
        }
    ),
    "XAF": Currency(
        **{
            "symbol": "FCFA",
            "name": "CFA Franc BEAC",
            "symbol_native": "FCFA",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "XAF",
            "name_plural": "CFA francs BEAC",
        }
    ),
    "XOF": Currency(
        **{
            "symbol": "CFA",
            "name": "CFA Franc BCEAO",
            "symbol_native": "CFA",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "XOF",
            "name_plural": "CFA francs BCEAO",
        }
    ),
    "YER": Currency(
        **{
            "symbol": "YR",
            "name": "Yemeni Rial",
            "symbol_native": "ر.ي.\u200f",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "YER",
            "name_plural": "Yemeni rials",
        }
    ),
    "ZAR": Currency(
        **{
            "symbol": "R",
            "name": "South African Rand",
            "symbol_native": "R",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "ZAR",
            "name_plural": "South African rand",
        }
    ),
    "ZMK": Currency(
        **{
            "symbol": "ZK",
            "name": "Zambian Kwacha",
            "symbol_native": "ZK",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "ZMK",
            "name_plural": "Zambian kwachas",
        }
    ),
}
