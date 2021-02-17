districts = [
    'কুমিল্লা', 'ফেনী', 'রাঙ্গামাটি', 'নোয়াখালী', 'চাঁদপুর', 'লক্ষ্মীপুর', 'চট্টগ্রাম',
    'কক্সবাজার', 'খাগড়াছড়ি', 'বান্দরবান', 'সিরাজগঞ্জ', 'পাবনা', 'বগুড়া', 'রাজশাহী', 'নাটোর', 'জয়পুরহাট',
    'চাঁপাইনবাবগঞ্জ', 'নওগাঁ', 'যশোর', 'সাতক্ষীরা', 'মেহেরপুর', 'চুয়াডাঙ্গা', 'কুষ্টিয়া', 'মাগুরা', 'খুলনা',
    'বাগেরহাট', 'ঝিনাইদহ', 'ঝালকাঠি', 'পটুয়াখালী', 'পিরোজপুর', 'বরিশাল', 'ভোলা', 'বরগুনা', 'সিলেট', 'মৌলভীবাজার',
    'হবিগঞ্জ', 'সুনামগঞ্জ', 'নরসিংদী', 'গাজীপুর', 'শরীয়তপুর', 'নারায়ণগঞ্জ', 'টাঙ্গাইল', 'কিশোরগঞ্জ',
    'মানিকগঞ্জ', 'ঢাকা', 'মুন্সিগঞ্জ', 'রাজবাড়ী', 'মাদারীপুর', 'গোপালগঞ্জ', 'ফরিদপুর', 'পঞ্চগড়', 'দিনাজপুর',
    'লালমনিরহাট', 'নীলফামারী', 'গাইবান্ধা', 'ঠাকুরগাঁও', 'রংপুর', 'কুড়িগ্রাম', 'শেরপুর', 'ময়মনসিংহ', 'জামালপুর',
    'নেত্রকোণা', 'পিরোজপুর', 'নেত্রকোনা', 'ব্রাহ্মণবাড়িয়া', 'নড়াইল', 'রাঙামাটি', 'নারায়াণগঞ্জ', 'চাঁপাই নবাবগঞ্জ',
    'শরীয়তপুর', 'লালমনরিহাট'
]


def get_district(reporter_info):
    for district in districts:
        if district in reporter_info:
            return district
    return ""
