from datetime import date
from .formfill import PdfDocument, PdfForm


class BasePDF(object):

    def __init__(self, instream, outstream):
        self.f = PdfForm(PdfDocument(instream, outstream))
        self.f.fields = ()
        self.data = {}

    def update(self, data, blob=''):
        print(blob, data)
        try:
            for k, v in data.items():
                if blob: k = "%s_%s" % (blob, k)

                if isinstance(v, (tuple, list, set, dict)):
                    self.update(v, blob=k)
                else:
                    self.data[k] = v
        except AttributeError:
            for i, v in enumerate(data):
                self.update(v, blob="%s_%s" % (blob, i))

    def save(self):
        self.f.fill(self.data)


class Main(BasePDF):

    def __init__(self, instream, outstream):
        super(Main, self).__init__(instream, outstream)
        f = self.f

        f.fields = ({
            'supervisor': f.shortans((235, 595)),
            'department': f.shortans((235, 560)),
            'given_name': f.shortans((326, 480)),
            'family_name': f.shortans((215, 480)),
            'middle_name': f.shortans((425, 480)),
            'given_name_kana': f.shortans((326, 417)),
            'family_name_kana': f.shortans((215, 417)),
            'middle_name_kana': f.shortans((425, 417)),
            'given_name_hanzi': f.shortans((340, 364)),
            'family_name_hanzi': f.shortans((215, 364)),
            'nationality': f.shortans((185, 297)),
            'birthdate' : f.date({'%Y': (310, 246), '%m': (130, 246), '%d': (220, 246)}),
            'age': f.shortans((410, 245), f.CENTER),
            'special_attention': f.longans((95, 140)),
            'present_address': f.shortans((95, 53)),
            'campus': f.checkbox({'KM': (92, 694), 'YS': (92, 643)}),
            'gender': f.checkbox({'M': (376, 294), 'F': (440, 294)}),
        }, {
            'permanent_address': f.shortans((90, 740)),
            'phone_number': f.shortans((200, 717)),
            'fax_number': f.shortans((440, 717)),
            'email': f.shortans((240, 701)),
            'emergency_0_name': f.shortans((90, 600)),
            'emergency_0_address': f.shortans((90, 550)),
            'emergency_0_phone_number': f.shortans((200, 515)),
            'emergency_0_fax_number': f.shortans((440, 515)),
            'emergency_0_email': f.shortans((235, 481)),
            'emergency_0_relation': f.shortans((250, 450)),
            'emergency_1_name': f.shortans((90, 381)),
            'emergency_1_address': f.shortans((90, 331)),
            'emergency_1_phone_number': f.shortans((200, 296)),
            'emergency_1_fax_number': f.shortans((440, 296)),
            'emergency_1_email': f.shortans((235, 262)),
            'emergency_1_relation': f.shortans((250, 231)),
            'school_current_name': f.shortans((90, 158)),
            'school_current_end': f.date({'%m': (345, 72), '%Y': (435, 72)}),
            'school_current_progress': f.checkbox({
                '6-1': (177, 121), '6-2': (252, 121), '6-3': (361, 121), '6-4': (471, 121),
                '7-1': (178, 104), '7-2': (252, 104),
                '8-1': (178, 87),  '8-2': (252, 87),  '8-3': (361, 87),
            }),
        }, {
            'school_1_name': f.shortans((70, 702)),
            'school_1_location': f.longans((295, 715)),
            'school_1_start': f.date({'%m': (377, 702), '%y': (398, 702)}),
            'school_1_end': f.date({'%m': (425, 702), '%y': (443, 702)}),
            'school_1_duration': f.shortans((520, 702), f.RIGHT),
            'school_2_name': f.shortans((70, 650)),
            'school_2_location': f.longans((295, 665)),
            'school_2_start': f.date({'%m': (377, 650), '%y': (398, 650)}),
            'school_2_end': f.date({'%m': (425, 650), '%y': (443, 650)}),
            'school_2_duration': f.shortans((520, 650), f.RIGHT),
            'school_3_name': f.shortans((70, 600)),
            'school_3_location': f.longans((295, 615)),
            'school_3_start': f.date({'%m': (377, 600), '%y': (398, 600)}),
            'school_3_end': f.date({'%m': (425, 600), '%y': (443, 600)}),
            'school_3_duration': f.shortans((520, 600), f.RIGHT),
            'school_6_name': f.shortans((70, 530)),
            'school_6_location': f.longans((295, 560)),
            'school_6_start': f.date({'%m': (377, 549), '%y': (398, 549)}),
            'school_6_end': f.date({'%m': (425, 549), '%y': (443, 549)}),
            'school_6_duration': f.shortans((520, 549), f.RIGHT),
            'school_7_name': f.shortans((70, 480)),
            'school_7_location': f.longans((295, 495)),
            'school_7_start': f.date({'%m': (377, 480), '%y': (398, 480)}),
            'school_7_end': f.date({'%m': (425, 480), '%y': (443, 480)}),
            'school_7_duration': f.shortans((520, 480), f.RIGHT),
            'school_8_name': f.shortans((70, 430)),
            'school_8_location': f.longans((295, 445)),
            'school_8_start': f.date({'%m': (377, 430), '%y': (398, 430)}),
            'school_8_end': f.date({'%m': (425, 430), '%y': (443, 430)}),
            'school_8_duration': f.shortans((520, 430), f.RIGHT),
            'school_total_duration': f.shortans((520, 412), f.RIGHT),
            'work_0_name': f.shortans((70, 270)),
            'work_0_location': f.shortans((280, 287)),
            'work_0_start': f.date({'%m': (381, 287), '%y': (400, 287)}),
            'work_0_end': f.date({'%m': (440, 287), '%y': (460, 287)}),
            'work_1_name': f.shortans((70, 237)),
            'work_1_location': f.shortans((280, 253)),
            'work_1_start': f.date({'%m': (381, 253), '%y': (400, 253)}),
            'work_1_end': f.date({'%m': (440, 253), '%y': (460, 253)}),
            'work_2_name': f.shortans((70, 202)),
            'work_2_location': f.shortans((280, 218)),
            'work_2_start': f.date({'%m': (381, 218), '%y': (400, 218)}),
            'work_2_end': f.date({'%m': (440, 218), '%y': (460, 218)}),
            'work_3_name': f.shortans((70, 170)),
            'work_3_location': f.shortans((280, 185)),
            'work_3_start': f.date({'%m': (381, 185), '%y': (400, 185)}),
            'work_3_end': f.date({'%m': (440, 185), '%y': (460, 185)}),
            'work_4_name': f.shortans((70, 135)),
            'work_4_location': f.shortans((280, 151)),
            'work_4_start': f.date({'%m': (381, 151), '%y': (400, 151)}),
            'work_4_end': f.date({'%m': (440, 151), '%y': (460, 151)}),
        }, {
            'language_0_reading': f.circle({5: (168, 706), 4: (186, 706), 3: (202, 706), 2: (220, 706), 1: (237, 706)}),
            'language_0_writing': f.circle({5: (260, 706), 4: (278, 706), 3: (295, 706), 2: (311, 706), 1: (330, 706)}), 
            'language_0_listening': f.circle({5: (355, 706), 4: (371, 706), 3: (387, 706), 2: (403, 706), 1: (421, 706)}), 
            'language_0_speaking': f.circle({5: (445, 706), 4: (461, 706), 3: (476, 706), 2: (494, 706), 1: (512, 706)}), 
            'language_1_reading': f.circle({5: (168, 682), 4: (186, 682), 3: (202, 682), 2: (220, 682), 1: (237, 682)}),
            'language_1_writing': f.circle({5: (260, 682), 4: (278, 682), 3: (295, 682), 2: (311, 682), 1: (330, 682)}), 
            'language_1_listening': f.circle({5: (355, 682), 4: (371, 682), 3: (387, 682), 2: (403, 682), 1: (421, 682)}), 
            'language_1_speaking': f.circle({5: (445, 682), 4: (461, 682), 3: (476, 682), 2: (494, 682), 1: (512, 682)}), 
            'language_2_name': f.shortans((110, 655)),
            'language_2_reading': f.circle({5: (168, 660), 4: (186, 660), 3: (202, 660), 2: (220, 660), 1: (237, 660)}),
            'language_2_writing': f.circle({5: (260, 660), 4: (278, 660), 3: (295, 660), 2: (311, 660), 1: (330, 660)}), 
            'language_2_listening': f.circle({5: (355, 660), 4: (371, 660), 3: (387, 660), 2: (403, 660), 1: (421, 660)}), 
            'language_2_speaking': f.circle({5: (445, 660), 4: (461, 660), 3: (476, 660), 2: (494, 660), 1: (512, 660)}), 
            'jlpt_0': f.checkbox({True: (92, 436), False: (92, 391)}),
            'jlpt_4': f.checkbox({True: (153, 421), False: (234, 421)}),
            'jlpt_3': f.checkbox({True: (368, 421), False: (471, 421)}),
            'jlpt_2': f.checkbox({True: (153, 407), False: (234, 407)}),
            'jlpt_1': f.checkbox({True: (368, 407), False: (471, 407)}),
            'english_test': f.checkbox({True: (92, 341), False: (92, 310)}),
            'start': f.date({'%m': (160, 243), '%Y': (235, 243)}),
            'end': f.date({'%m': (350, 243), '%Y': (420, 243)}),
        }, {
            'field_of_study': f.longans((90, 640)),
            'study_plans': f.longans((90, 370)),
        })

    def process(self, user):
        self.update(user.details)
        self.update(user.person.details)
        self.update(user.enrollment.details)


class Visa(BasePDF):

    def __init__(self, instream, outstream):
        super(Visa, self).__init__(instream, outstream)
        f = self.f

        f.fields = ({
            'family_name': f.shortans((105, 660)),
            'given_name': f.shortans((270, 660), f.RIGHT),
            'birthdate' : f.date({'%Y': (385, 660), '%m': (440, 660), '%d': (490, 660)}),
            'nationality': f.shortans((100, 635)),
            'gender': f.circle({'M': (92, 616), 'F': (127, 616)}),
            'maritial': f.circle({True: (464, 616), False: (499, 616)}),
            'place_of_birth': f.shortans((230, 615)),
            'occupation': f.shortans((85, 591)),
            'hometown': f.shortans((300, 591)),
            'japan_address': f.longans((130, 571)),
            'telephone_number': f.shortans((130, 551)),
            'mobile_number': f.shortans((355, 551)),
            'passport_number': f.shortans((130, 531)),
            'passport_expiry': f.date({'%Y': (385, 531), '%m': (440, 531), '%d': (490, 531)}),
            'purpose': f.checkbox({'P': (304, 450)}),
            'entry_port': f.shortans((370, 368)),
            'entry_date': f.date({'%Y': (140, 368), '%m': (195, 368), '%d': (240, 368)}),
            'stay_days': f.shortans((140, 348)),
            'application_place': f.shortans((140, 326)),
            'accompanying': f.circle({True: (412, 351), False: (435, 351)}),
            'past_entrance': f.circle({True: (180, 310), False: (202, 310)}),
            'past_entries': f.shortans((100, 280), f.RIGHT),
            'last_entry': f.date({'%Y': (235, 280), '%m': (290, 280), '%d': (335, 280)}),
            'last_exit': f.date({'%Y': (395, 280), '%m': (450, 280), '%d': (495, 280)}),
            'past_criminal': f.circle({True: (62, 253), False: (494, 253)}),
            'past_deportation': f.circle({True: (237, 233), False: (260, 233)}),
        }, {
            'school_current_name': f.shortans((128, 780)),
            'school_current_phone': f.shortans((390, 755)),
            'school_current_location': f.shortans((118, 755)),
            'school_total_duration': f.shortans((345, 730)),
            'school_current_name_short': f.shortans((139, 620)),
            'school_current_end': f.date({'%m': (465, 620), '%Y': (410, 620)}),
            'school_current_status': f.checkbox({'C': (213, 702)}),
            'school_current_level': f.checkbox({
                8: (71, 680), 7: (172, 680), 6: (271, 680), 4: (345, 680),
                3: (71, 655), 2: (172, 655), 1: (257, 655), 0: (345, 655),
            }),
            'expenses': f.checkbox({'H': (55, 290)}),
        })

        self.update({
            'maritial': False,
            'japan_address': "〒861-1102 熊本県, 合志市須屋 ２６５９－２熊本高専明和寮南棟",
            'telephone_number': "096-242-6253",
            'accompanying': False,
            'past_criminal': False,
            'past_deportation': False,
            'purpose': 'P',
            'education_status': 'C',
            'expenses': 'H',
            'graduation_plan': 'R',
        })

    def process(self, user):
        self.update(user.details)
        self.update(user.person.details)
        self.update(user.enrollment.details)
        self.update(user.visaapplication.details)


class Dorm(BasePDF):

    def __init__(self, instream, outstream):
        super(Dorm, self).__init__(instream, outstream)
        f = self.f

        f.fields = ({
            'full_name': f.shortans((160, 650)),
            'school_current_name': f.shortans((165, 615)),
            'emergency_0_relation': f.shortans((180, 545)),
            'emergency_0_phone_number': f.shortans((180, 513)),
            'emergency_0_fax_number': f.shortans((371, 513)),
            'emergency_0_address': f.shortans((155, 480)),
            'special': f.shortans((240, 429)),
            'start': f.date({'%Y': (436, 380), '%m': (390, 380), '%d': (340, 380)}),
            'end': f.date({'%Y': (436, 345), '%m': (390, 345), '%d': (340, 345)}),
        },)

    def process(self, user):
        self.update(user.details)
        self.update(user.person.details)
        self.update(user.enrollment.details)
