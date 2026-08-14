use mimir_replay::{
    ReplayNetworkAttributeTagV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkK3ValueV1,
    ReplayNetworkVector3V1, decode_replay_network_k3_v1,
};

const LOCATION_CODES: &[u32] = &[7, 8, 14, 15, 16, 17, 32, 39, 40, 46, 47];

const RIGID_BODY_CODES: &[u32] = &[
    10635, 10666, 10667, 10669, 10703, 10734, 11691, 11693, 11714, 11715, 11725, 11727, 11756,
    11757, 11758, 11759, 11784, 11788, 11789, 11790, 11791, 11822, 11823, 12417, 12418, 12582,
    12647, 12687, 12712, 12717, 12718, 12719, 12742, 12748, 12749, 12750, 12751, 12778, 12779,
    12780, 12781, 12782, 12783, 12802, 12803, 12804, 12806, 12807, 12808, 12809, 12810, 12812,
    12813, 12814, 12815, 12835, 12837, 12838, 12839, 12842, 12845, 12846, 12847, 12879, 13312,
    13576, 13632, 13642, 13664, 13674, 13675, 13679, 13696, 13708, 13710, 13711, 13728, 13736,
    13738, 13739, 13740, 13741, 13742, 13743, 13769, 13770, 13771, 13772, 13773, 13774, 13775,
    13798, 13800, 13801, 13802, 13803, 13804, 13805, 13806, 13807, 13826, 13829, 13830, 13831,
    13832, 13833, 13834, 13835, 13836, 13837, 13838, 13839, 13859, 13861, 13863, 13864, 13865,
    13866, 13867, 13868, 13869, 13870, 13871, 13899, 13900, 13901, 13902, 13903, 14467, 14597,
    14671, 14700, 14703, 14727, 14734, 14735, 14762, 14763, 14764, 14765, 14766, 14767, 14788,
    14790, 14792, 14794, 14795, 14796, 14797, 14798, 14799, 14818, 14820, 14821, 14823, 14824,
    14825, 14826, 14827, 14828, 14829, 14830, 14831, 14850, 14852, 14853, 14854, 14855, 14856,
    14857, 14858, 14859, 14860, 14861, 14862, 14863, 14881, 14883, 14884, 14885, 14886, 14887,
    14888, 14889, 14890, 14891, 14892, 14893, 14894, 14895, 14923, 14925, 14926, 14927, 15524,
    15554, 15559, 15682, 15687, 15719, 15722, 15750, 15755, 15756, 15757, 15758, 15759, 15782,
    15785, 15786, 15787, 15788, 15789, 15790, 15791, 15813, 15814, 15816, 15817, 15818, 15819,
    15820, 15821, 15822, 15823, 15842, 15844, 15845, 15846, 15847, 15848, 15849, 15850, 15851,
    15852, 15853, 15854, 15855, 15872, 15873, 15874, 15875, 15876, 15877, 15878, 15879, 15880,
    15881, 15882, 15883, 15884, 15885, 15886, 15887, 15904, 15905, 15906, 15907, 15908, 15909,
    15910, 15911, 15912, 15913, 15914, 15915, 15916, 15917, 15918, 15919, 15947, 15949, 15950,
    15951, 16384, 16392, 16418, 16523, 16548, 16554, 16583, 16585, 16586, 16609, 16613, 16616,
    16618, 16619, 16645, 16647, 16650, 16651, 16652, 16677, 16679, 16680, 16681, 16682, 16683,
    16711, 16712, 16713, 16714, 16715, 16716, 16717, 16718, 16719, 16740, 16743, 16744, 16745,
    16746, 16747, 16748, 16749, 16770, 16774, 16775, 16776, 16777, 16778, 16779, 16780, 16781,
    16782, 16783, 16802, 16803, 16804, 16806, 16807, 16808, 16809, 16810, 16811, 16812, 16813,
    16814, 16815, 16833, 16834, 16835, 16836, 16837, 16838, 16839, 16840, 16841, 16842, 16843,
    16844, 16845, 16846, 16847, 16864, 16865, 16866, 16867, 16868, 16869, 16870, 16871, 16872,
    16873, 16874, 16875, 16876, 16877, 16878, 16879, 16896, 16897, 16898, 16899, 16900, 16901,
    16902, 16903, 16904, 16905, 16906, 16907, 16908, 16909, 16910, 16911, 16928, 16929, 16930,
    16931, 16932, 16933, 16934, 16935, 16936, 16937, 16938, 16939, 16940, 16941, 16942, 16943,
    16971, 16973, 16974, 16975, 17476, 17537, 17538, 17540, 17570, 17633, 17635, 17636, 17637,
    17640, 17668, 17669, 17672, 17673, 17674, 17696, 17699, 17701, 17702, 17704, 17728, 17730,
    17731, 17732, 17737, 17738, 17739, 17740, 17741, 17742, 17743, 17760, 17762, 17763, 17764,
    17765, 17766, 17767, 17768, 17769, 17770, 17771, 17772, 17773, 17774, 17792, 17794, 17795,
    17796, 17797, 17798, 17799, 17800, 17801, 17802, 17803, 17804, 17805, 17807, 17824, 17825,
    17826, 17828, 17829, 17830, 17831, 17832, 17833, 17834, 17835, 17836, 17837, 17838, 17839,
    17856, 17857, 17858, 17859, 17860, 17861, 17862, 17863, 17864, 17865, 17866, 17867, 17868,
    17869, 17870, 17871, 17888, 17889, 17890, 17891, 17892, 17893, 17894, 17895, 17896, 17897,
    17898, 17899, 17900, 17901, 17902, 17903, 17920, 17921, 17922, 17923, 17924, 17925, 17926,
    17927, 17928, 17929, 17930, 17931, 17932, 17933, 17934, 17935, 17952, 17953, 17954, 17955,
    17956, 17957, 17958, 17959, 17960, 17961, 17962, 17963, 17964, 17965, 17966, 17967, 17997,
    17998, 17999, 18500, 18560, 18561, 18562, 18563, 18564, 18594, 18595, 18628, 18630, 18633,
    18661, 18662, 18663, 18690, 18691, 18692, 18693, 18695, 18696, 18697, 18698, 18700, 18720,
    18721, 18723, 18724, 18725, 18726, 18727, 18728, 18729, 18730, 18731, 18732, 18752, 18755,
    18756, 18757, 18758, 18759, 18760, 18761, 18762, 18763, 18764, 18767, 18784, 18785, 18786,
    18787, 18788, 18789, 18790, 18791, 18792, 18793, 18794, 18795, 18796, 18797, 18798, 18799,
    18816, 18817, 18818, 18819, 18820, 18821, 18822, 18823, 18824, 18825, 18826, 18827, 18828,
    18829, 18830, 18831, 18848, 18849, 18850, 18851, 18852, 18853, 18854, 18855, 18856, 18857,
    18858, 18859, 18860, 18861, 18862, 18863, 18881, 18882, 18883, 18884, 18885, 18886, 18887,
    18888, 18889, 18890, 18891, 18892, 18893, 18894, 18895, 18912, 18913, 18914, 18915, 18916,
    18917, 18918, 18919, 18920, 18921, 18922, 18923, 18924, 18925, 18926, 18927, 18944, 18945,
    18946, 18947, 18948, 18949, 18950, 18951, 18952, 18953, 18954, 18955, 18956, 18957, 18958,
    18959, 18976, 18977, 18978, 18979, 18980, 18981, 18982, 18983, 18984, 18985, 18986, 18987,
    18988, 18989, 18990, 18991, 19020, 19021, 19022, 19023, 19556, 19618, 19620, 19621, 19622,
    19651, 19654, 19685, 19686, 19687, 19717, 19719, 19746, 19747, 19748, 19750, 19752, 19753,
    19778, 19780, 19781, 19783, 19784, 19786, 19788, 19790, 19809, 19810, 19811, 19812, 19813,
    19814, 19815, 19817, 19818, 19819, 19820, 19841, 19842, 19843, 19844, 19845, 19846, 19847,
    19848, 19849, 19850, 19851, 19852, 19853, 19854, 19872, 19874, 19875, 19876, 19877, 19878,
    19879, 19880, 19881, 19882, 19883, 19884, 19885, 19886, 19887, 19904, 19905, 19906, 19907,
    19908, 19909, 19910, 19911, 19912, 19913, 19914, 19915, 19916, 19917, 19918, 19919, 19937,
    19938, 19939, 19940, 19941, 19942, 19943, 19944, 19945, 19946, 19947, 19948, 19949, 19950,
    19951, 19969, 19970, 19971, 19973, 19974, 19975, 19976, 19977, 19978, 19979, 19980, 19981,
    19982, 19983, 20008, 20009, 20010, 20011, 20012, 20013, 20014, 20015, 47103, 50175, 51199,
    52223, 76237, 76260, 76261, 76270, 76294, 76296, 76299, 76300, 76301, 76302, 76327, 76330,
    76333, 76965, 76999, 77032, 77248, 77260, 77261, 77262, 77263, 77282, 77290, 77291, 77293,
    77294, 77295, 77319, 77320, 77321, 77322, 77323, 77324, 77325, 77326, 77327, 77347, 77351,
    77355, 77356, 77357, 77358, 77390, 77391, 77987, 78176, 78208, 78215, 78219, 78221, 78222,
    78223, 78240, 78249, 78250, 78251, 78252, 78253, 78254, 78255, 78272, 78280, 78284, 78285,
    78286, 78287, 78306, 78308, 78311, 78312, 78314, 78315, 78316, 78317, 78318, 78319, 78338,
    78339, 78340, 78342, 78343, 78344, 78345, 78346, 78347, 78348, 78349, 78350, 78351, 78370,
    78371, 78372, 78373, 78374, 78376, 78377, 78378, 78379, 78380, 78381, 78382, 78383, 78848,
    78980, 79008, 79078, 79112, 79117, 79149, 79151, 79168, 79175, 79178, 79183, 79200, 79202,
    79204, 79207, 79210, 79211, 79213, 79214, 79215, 79232, 79234, 79239, 79240, 79241, 79243,
    79244, 79245, 79246, 79247, 79264, 79266, 79271, 79272, 79274, 79275, 79276, 79277, 79278,
    79279, 79301, 79302, 79303, 79304, 79305, 79306, 79307, 79308, 79309, 79310, 79311, 79330,
    79331, 79332, 79333, 79334, 79335, 79336, 79337, 79338, 79339, 79340, 79341, 79342, 79343,
    79362, 79363, 79364, 79365, 79366, 79367, 79368, 79369, 79370, 79371, 79372, 79373, 79374,
    79375, 79394, 79395, 79396, 79397, 79398, 79399, 79400, 79401, 79402, 79403, 79404, 79405,
    79406, 79407, 79433, 79435, 79436, 79437, 79438, 79439, 80033, 80066, 80099, 80169, 80173,
    80194, 80201, 80202, 80203, 80205, 80206, 80207, 80230, 80233, 80235, 80236, 80237, 80238,
    80239, 80258, 80260, 80261, 80263, 80264, 80266, 80267, 80268, 80269, 80270, 80271, 80290,
    80293, 80295, 80296, 80297, 80298, 80299, 80300, 80301, 80302, 80303, 80322, 80324, 80325,
    80326, 80327, 80328, 80329, 80330, 80331, 80332, 80333, 80334, 80335, 80353, 80354, 80355,
    80356, 80357, 80358, 80359, 80360, 80361, 80362, 80363, 80364, 80365, 80366, 80367, 80385,
    80386, 80387, 80388, 80389, 80390, 80391, 80392, 80393, 80394, 80395, 80396, 80397, 80398,
    80399, 80417, 80418, 80419, 80420, 80421, 80422, 80423, 80424, 80425, 80426, 80427, 80428,
    80429, 80430, 80431, 80457, 80460, 80461, 80462, 80463, 81024, 81027, 81058, 81127, 81188,
    81192, 81195, 81219, 81225, 81227, 81228, 81250, 81251, 81253, 81254, 81255, 81256, 81259,
    81260, 81261, 81282, 81285, 81288, 81289, 81291, 81292, 81293, 81294, 81295, 81312, 81314,
    81315, 81317, 81318, 81319, 81320, 81321, 81322, 81323, 81324, 81325, 81326, 81327, 81346,
    81348, 81349, 81350, 81351, 81352, 81353, 81354, 81355, 81356, 81357, 81358, 81359, 81376,
    81377, 81378, 81379, 81380, 81381, 81382, 81383, 81384, 81385, 81386, 81387, 81388, 81389,
    81390, 81391, 81408, 81409, 81410, 81411, 81412, 81413, 81414, 81415, 81416, 81417, 81418,
    81419, 81420, 81421, 81422, 81423, 81440, 81441, 81442, 81443, 81444, 81445, 81446, 81447,
    81448, 81449, 81450, 81451, 81452, 81453, 81454, 81455, 81481, 81484, 81485, 81486, 81487,
    82016, 82048, 82049, 82050, 82051, 82081, 82082, 82083, 82084, 82085, 82114, 82117, 82149,
    82176, 82179, 82184, 82211, 82212, 82217, 82219, 82240, 82242, 82243, 82247, 82248, 82249,
    82250, 82251, 82252, 82272, 82273, 82274, 82276, 82278, 82279, 82281, 82282, 82283, 82284,
    82287, 82304, 82305, 82306, 82307, 82308, 82309, 82312, 82313, 82314, 82315, 82316, 82317,
    82318, 82336, 82337, 82338, 82339, 82340, 82341, 82342, 82343, 82344, 82345, 82346, 82347,
    82348, 82349, 82350, 82351, 82368, 82369, 82370, 82371, 82372, 82373, 82374, 82375, 82376,
    82377, 82378, 82379, 82380, 82381, 82382, 82383, 82400, 82401, 82402, 82403, 82404, 82405,
    82406, 82407, 82408, 82409, 82410, 82411, 82412, 82413, 82414, 82415, 82432, 82433, 82434,
    82435, 82436, 82437, 82438, 82439, 82440, 82441, 82442, 82443, 82444, 82445, 82446, 82447,
    82464, 82465, 82466, 82467, 82468, 82469, 82470, 82471, 82472, 82473, 82474, 82475, 82476,
    82477, 82478, 82479, 82505, 82508, 82509, 82510, 82511, 83042, 83072, 83073, 83074, 83075,
    83076, 83077, 83105, 83106, 83107, 83108, 83137, 83139, 83142, 83143, 83170, 83171, 83172,
    83173, 83174, 83175, 83202, 83203, 83204, 83205, 83206, 83207, 83208, 83210, 83211, 83232,
    83233, 83234, 83235, 83236, 83237, 83238, 83239, 83240, 83241, 83242, 83243, 83247, 83264,
    83265, 83266, 83267, 83268, 83269, 83270, 83271, 83272, 83273, 83274, 83275, 83276, 83279,
    83296, 83297, 83298, 83299, 83300, 83301, 83302, 83303, 83304, 83305, 83306, 83307, 83308,
    83309, 83310, 83311, 83328, 83329, 83330, 83331, 83332, 83333, 83334, 83335, 83336, 83337,
    83338, 83339, 83340, 83341, 83342, 83343, 83360, 83361, 83362, 83363, 83364, 83365, 83366,
    83367, 83368, 83369, 83370, 83371, 83372, 83373, 83374, 83375, 83392, 83393, 83394, 83395,
    83396, 83397, 83398, 83399, 83400, 83401, 83402, 83403, 83404, 83405, 83406, 83407, 83424,
    83425, 83426, 83427, 83428, 83429, 83430, 83431, 83432, 83433, 83434, 83435, 83436, 83437,
    83438, 83439, 83456, 83457, 83458, 83459, 83460, 83461, 83462, 83463, 83464, 83465, 83466,
    83467, 83468, 83469, 83470, 83471, 83488, 83489, 83490, 83491, 83492, 83493, 83494, 83495,
    83496, 83497, 83498, 83499, 83500, 83501, 83502, 83503, 83529, 83532, 83533, 83534, 83535,
    83970, 84064, 84065, 84066, 84096, 84097, 84098, 84099, 84100, 84101, 84128, 84129, 84130,
    84131, 84132, 84133, 84134, 84135, 84161, 84162, 84163, 84164, 84165, 84166, 84167, 84169,
    84170, 84171, 84192, 84193, 84194, 84195, 84196, 84197, 84198, 84199, 84201, 84202, 84225,
    84226, 84227, 84228, 84229, 84230, 84231, 84232, 84233, 84234, 84235, 84236, 84256, 84257,
    84258, 84259, 84260, 84261, 84262, 84263, 84264, 84265, 84266, 84267, 84268, 84288, 84289,
    84290, 84291, 84292, 84293, 84294, 84295, 84296, 84297, 84298, 84299, 84300, 84301, 84303,
    84320, 84321, 84322, 84323, 84324, 84325, 84326, 84327, 84328, 84329, 84330, 84331, 84332,
    84333, 84334, 84335, 84352, 84353, 84354, 84355, 84356, 84357, 84358, 84359, 84360, 84361,
    84362, 84363, 84364, 84365, 84366, 84367, 84384, 84385, 84386, 84387, 84388, 84389, 84390,
    84391, 84392, 84393, 84394, 84395, 84396, 84397, 84398, 84399, 84416, 84417, 84418, 84419,
    84420, 84421, 84422, 84423, 84424, 84425, 84426, 84427, 84428, 84429, 84430, 84431, 84448,
    84449, 84450, 84451, 84452, 84453, 84454, 84455, 84456, 84457, 84458, 84459, 84460, 84461,
    84462, 84463, 84480, 84481, 84482, 84483, 84484, 84485, 84486, 84487, 84488, 84489, 84490,
    84491, 84492, 84493, 84494, 84495, 84512, 84513, 84514, 84515, 84516, 84517, 84518, 84519,
    84520, 84521, 84522, 84523, 84524, 84525, 84526, 84527, 84553, 84554, 84555, 84556, 84557,
    84558, 84559, 84992, 85056, 85090, 85092, 85093, 85120, 85122, 85123, 85124, 85125, 85152,
    85153, 85154, 85155, 85156, 85157, 85158, 85159, 85185, 85186, 85187, 85188, 85189, 85190,
    85217, 85218, 85219, 85220, 85221, 85222, 85223, 85224, 85251, 85252, 85253, 85254, 85255,
    85256, 85257, 85258, 85261, 85282, 85283, 85284, 85285, 85286, 85287, 85288, 85289, 85290,
    85291, 85292, 85312, 85313, 85314, 85315, 85316, 85317, 85318, 85319, 85320, 85321, 85322,
    85323, 85324, 85325, 85327, 85344, 85345, 85346, 85347, 85348, 85349, 85350, 85351, 85352,
    85353, 85354, 85355, 85356, 85357, 85358, 85359, 85376, 85377, 85378, 85379, 85380, 85381,
    85382, 85383, 85384, 85385, 85386, 85387, 85388, 85389, 85390, 85391, 85408, 85409, 85410,
    85411, 85412, 85413, 85414, 85415, 85416, 85417, 85418, 85419, 85420, 85421, 85422, 85423,
    85440, 85441, 85442, 85443, 85444, 85445, 85446, 85447, 85448, 85449, 85450, 85451, 85452,
    85453, 85454, 85455, 85472, 85473, 85474, 85475, 85476, 85477, 85478, 85479, 85480, 85481,
    85482, 85483, 85484, 85485, 85486, 85487, 85505, 85506, 85507, 85508, 85509, 85510, 85511,
    85512, 85513, 85514, 85515, 85516, 85517, 85518, 85519, 85538, 85543, 85544, 85545, 85546,
    85547, 85548, 85549, 85550, 85551, 112639, 115711, 116735, 117759, 118783,
];

const PICKUP_NEW_CODES: &[u32] = &[0, 1, 2, 3];

const REPLICATED_BOOST_CODES: &[u32] = &[1];

#[derive(Default)]
struct BitWriter {
    bits: Vec<bool>,
}

impl BitWriter {
    fn push_bits(&mut self, value: u64, width: usize) {
        for bit in 0..width {
            self.bits.push(((value >> bit) & 1) != 0);
        }
    }

    fn len(&self) -> usize {
        self.bits.len()
    }

    fn into_bytes(self) -> Vec<u8> {
        let mut bytes = vec![0u8; self.bits.len().div_ceil(8)];
        for (index, bit) in self.bits.into_iter().enumerate() {
            if bit {
                bytes[index / 8] |= 1 << (index % 8);
            }
        }
        bytes
    }
}

fn context(rl223: bool) -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: rl223,
    }
}

fn begin_unaligned() -> BitWriter {
    let mut writer = BitWriter::default();
    writer.push_bits(0b101, 3);
    writer
}

fn write_vector(writer: &mut BitWriter, size: u8) {
    match size {
        0..=5 => {
            writer.push_bits(u64::from(size), 4);
            writer.push_bits(0, 1);
        }
        6..=15 => writer.push_bits(u64::from(size), 4),
        16..=21 => {
            writer.push_bits(u64::from(size - 16), 4);
            writer.push_bits(1, 1);
        }
        _ => panic!("synthetic vector size outside current finite domain: {size}"),
    }
    let width = usize::from(size + 2);
    let bias = 1u64 << (size + 1);
    writer.push_bits(bias, width);
    writer.push_bits(bias, width);
    writer.push_bits(bias, width);
}

fn write_valid_quat56(writer: &mut BitWriter) {
    writer.push_bits(0, 2);
    writer.push_bits(131_072, 18);
    writer.push_bits(131_072, 18);
    writer.push_bits(131_072, 18);
}

fn write_invalid_quat56(writer: &mut BitWriter) {
    writer.push_bits(0, 2);
    writer.push_bits(262_143, 18);
    writer.push_bits(262_143, 18);
    writer.push_bits(262_143, 18);
}

fn rigid_fields(code: u32) -> (bool, bool, u8, u8, u8) {
    (
        ((code >> 16) & 1) != 0,
        ((code >> 15) & 1) != 0,
        ((code >> 10) & 0x1f) as u8,
        ((code >> 5) & 0x1f) as u8,
        (code & 0x1f) as u8,
    )
}

fn write_rigid_payload(writer: &mut BitWriter, code: u32) {
    let (_, sleeping, location, linear, angular) = rigid_fields(code);
    writer.push_bits(sleeping as u64, 1);
    write_vector(writer, location);
    write_valid_quat56(writer);
    if !sleeping {
        write_vector(writer, linear);
        write_vector(writer, angular);
    }
}

fn assert_zero_vector(value: &ReplayNetworkVector3V1, expected_size: u8) {
    assert_eq!(value.selected_size_bits, expected_size);
    assert_eq!(value.component_width, expected_size + 2);
    let bias = 1u32 << (expected_size + 1);
    assert_eq!((value.raw_x, value.raw_y, value.raw_z), (bias, bias, bias));
    assert_eq!(value.x.to_bits(), 0.0_f32.to_bits());
    assert_eq!(value.y.to_bits(), 0.0_f32.to_bits());
    assert_eq!(value.z.to_bits(), 0.0_f32.to_bits());
}

fn assert_error_category<T: std::fmt::Debug>(result: mimir_core::Result<T>, category: &str) {
    let error = result.expect_err("decode should fail closed");
    let message = error.to_string();
    assert!(
        message.contains(category),
        "expected error category {category:?}, got {message:?}"
    );
}

#[test]
fn every_r3_17j_admitted_group_has_a_synthetic_positive() {
    let mut positive_count = 0usize;

    for &code in LOCATION_CODES {
        let rl223 = ((code >> 5) & 1) != 0;
        let size = (code & 0x1f) as u8;
        let mut writer = begin_unaligned();
        write_vector(&mut writer, size);
        let expected_end = writer.len();
        writer.push_bits(0b1_1010, 5);
        let decoded = decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::Location,
            context(rl223),
        )
        .expect("admitted Location must decode");
        assert_eq!(decoded.payload_end_bit, expected_end as u64);
        assert_eq!(decoded.payload_width, (expected_end - 3) as u64);
        match decoded.value {
            ReplayNetworkK3ValueV1::Location(value) => assert_zero_vector(&value, size),
            other => panic!("unexpected Location variant: {other:?}"),
        }
        positive_count += 1;
    }

    for &code in RIGID_BODY_CODES {
        let (rl223, sleeping, location, linear, angular) = rigid_fields(code);
        let mut writer = begin_unaligned();
        write_rigid_payload(&mut writer, code);
        let expected_end = writer.len();
        writer.push_bits(0b10101, 5);
        let decoded = decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::RigidBody,
            context(rl223),
        )
        .expect("admitted RigidBody must decode");
        assert_eq!(decoded.payload_end_bit, expected_end as u64);
        match decoded.value {
            ReplayNetworkK3ValueV1::RigidBody(value) => {
                assert_eq!(value.sleeping, sleeping);
                assert_zero_vector(&value.location, location);
                assert_eq!(value.rotation.largest, 0);
                assert_eq!(
                    (
                        value.rotation.raw_a,
                        value.rotation.raw_b,
                        value.rotation.raw_c
                    ),
                    (131_072, 131_072, 131_072)
                );
                let norm = value.rotation.x * value.rotation.x
                    + value.rotation.y * value.rotation.y
                    + value.rotation.z * value.rotation.z
                    + value.rotation.w * value.rotation.w;
                assert!((norm - 1.0).abs() < 0.0001, "quaternion norm {norm}");
                if sleeping {
                    assert!(value.linear_velocity.is_none());
                    assert!(value.angular_velocity.is_none());
                    assert_eq!((linear, angular), (31, 31));
                } else {
                    assert_zero_vector(value.linear_velocity.as_ref().unwrap(), linear);
                    assert_zero_vector(value.angular_velocity.as_ref().unwrap(), angular);
                }
            }
            other => panic!("unexpected RigidBody variant: {other:?}"),
        }
        positive_count += 1;
    }

    for &code in PICKUP_NEW_CODES {
        let rl223 = ((code >> 1) & 1) != 0;
        let some = (code & 1) != 0;
        let mut writer = begin_unaligned();
        writer.push_bits(some as u64, 1);
        if some {
            writer.push_bits((-123_i32) as u32 as u64, 32);
        }
        writer.push_bits(0xA5, 8);
        let expected_end = writer.len();
        writer.push_bits(0b10101, 5);
        let decoded = decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::PickupNew,
            context(rl223),
        )
        .expect("admitted PickupNew must decode");
        assert_eq!(decoded.payload_end_bit, expected_end as u64);
        match decoded.value {
            ReplayNetworkK3ValueV1::PickupNew(value) => {
                assert_eq!(value.instigator, some.then_some(-123));
                assert_eq!(value.picked_up, 0xA5);
            }
            other => panic!("unexpected PickupNew variant: {other:?}"),
        }
        positive_count += 1;
    }

    for &code in REPLICATED_BOOST_CODES {
        let rl223 = code != 0;
        let mut writer = begin_unaligned();
        for value in [1u64, 2, 3, 4] {
            writer.push_bits(value, 8);
        }
        let expected_end = writer.len();
        writer.push_bits(0b10101, 5);
        let decoded = decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::ReplicatedBoost,
            context(rl223),
        )
        .expect("admitted ReplicatedBoost must decode");
        assert_eq!(decoded.payload_end_bit, expected_end as u64);
        assert_eq!(decoded.payload_width, 32);
        match decoded.value {
            ReplayNetworkK3ValueV1::ReplicatedBoost(value) => assert_eq!(
                (
                    value.grant_count,
                    value.boost_amount,
                    value.unused1,
                    value.unused2
                ),
                (1, 2, 3, 4)
            ),
            other => panic!("unexpected ReplicatedBoost variant: {other:?}"),
        }
        positive_count += 1;
    }

    assert_eq!(positive_count, 1_950);
}

#[test]
fn structural_acceptance_is_exactly_the_r3_17j_allowlist() {
    for rl223 in [false, true] {
        for size in 0u8..=21 {
            let code = ((rl223 as u32) << 5) | u32::from(size);
            let mut writer = begin_unaligned();
            write_vector(&mut writer, size);
            let result = decode_replay_network_k3_v1(
                &writer.into_bytes(),
                3,
                ReplayNetworkAttributeTagV1::Location,
                context(rl223),
            );
            assert_eq!(
                result.is_ok(),
                size < 20 && LOCATION_CODES.binary_search(&code).is_ok(),
                "Location code {code}"
            );
        }
    }

    for rl223 in [false, true] {
        for sleeping in [false, true] {
            for location in 0u8..=21 {
                if sleeping {
                    let code = ((rl223 as u32) << 16)
                        | (1 << 15)
                        | (u32::from(location) << 10)
                        | (31 << 5)
                        | 31;
                    let mut writer = begin_unaligned();
                    writer.push_bits(1, 1);
                    write_vector(&mut writer, location);
                    write_valid_quat56(&mut writer);
                    let result = decode_replay_network_k3_v1(
                        &writer.into_bytes(),
                        3,
                        ReplayNetworkAttributeTagV1::RigidBody,
                        context(rl223),
                    );
                    assert_eq!(
                        result.is_ok(),
                        location < 20 && RIGID_BODY_CODES.binary_search(&code).is_ok(),
                        "sleeping RigidBody code {code}"
                    );
                    continue;
                }

                for linear in 0u8..=21 {
                    for angular in 0u8..=21 {
                        let code = ((rl223 as u32) << 16)
                            | (u32::from(location) << 10)
                            | (u32::from(linear) << 5)
                            | u32::from(angular);
                        let mut writer = begin_unaligned();
                        writer.push_bits(0, 1);
                        write_vector(&mut writer, location);
                        write_valid_quat56(&mut writer);
                        write_vector(&mut writer, linear);
                        write_vector(&mut writer, angular);
                        let result = decode_replay_network_k3_v1(
                            &writer.into_bytes(),
                            3,
                            ReplayNetworkAttributeTagV1::RigidBody,
                            context(rl223),
                        );
                        let field_sizes_admitted = location < 20 && linear < 20 && angular < 20;
                        assert_eq!(
                            result.is_ok(),
                            field_sizes_admitted && RIGID_BODY_CODES.binary_search(&code).is_ok(),
                            "awake RigidBody code {code}"
                        );
                    }
                }
            }
        }
    }

    for rl223 in [false, true] {
        for some in [false, true] {
            let code = ((rl223 as u32) << 1) | (some as u32);
            let mut writer = begin_unaligned();
            writer.push_bits(some as u64, 1);
            if some {
                writer.push_bits(7, 32);
            }
            writer.push_bits(9, 8);
            let result = decode_replay_network_k3_v1(
                &writer.into_bytes(),
                3,
                ReplayNetworkAttributeTagV1::PickupNew,
                context(rl223),
            );
            assert_eq!(
                result.is_ok(),
                PICKUP_NEW_CODES.binary_search(&code).is_ok(),
                "PickupNew code {code}"
            );
        }
    }

    for rl223 in [false, true] {
        let code = rl223 as u32;
        let mut writer = begin_unaligned();
        for value in [1u64, 2, 3, 4] {
            writer.push_bits(value, 8);
        }
        let result = decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::ReplicatedBoost,
            context(rl223),
        );
        assert_eq!(
            result.is_ok(),
            REPLICATED_BOOST_CODES.binary_search(&code).is_ok(),
            "ReplicatedBoost code {code}"
        );
    }
}

#[test]
fn context_start_tag_and_truncation_fail_closed() {
    let valid_location_code = LOCATION_CODES[0];
    let rl223 = ((valid_location_code >> 5) & 1) != 0;
    let size = (valid_location_code & 0x1f) as u8;
    let mut writer = begin_unaligned();
    write_vector(&mut writer, size);
    let bytes = writer.into_bytes();

    for bad in [
        ReplayNetworkK3DecodeContextV1 {
            version_major: 867,
            ..context(rl223)
        },
        ReplayNetworkK3DecodeContextV1 {
            version_minor: 31,
            ..context(rl223)
        },
        ReplayNetworkK3DecodeContextV1 {
            net_version: 9,
            ..context(rl223)
        },
    ] {
        assert_error_category(
            decode_replay_network_k3_v1(&bytes, 3, ReplayNetworkAttributeTagV1::Location, bad),
            "unadmitted-context",
        );
    }

    assert_error_category(
        decode_replay_network_k3_v1(
            &bytes,
            (bytes.len() as u64) * 8 + 1,
            ReplayNetworkAttributeTagV1::Location,
            context(rl223),
        ),
        "invalid-start",
    );

    assert_error_category(
        decode_replay_network_k3_v1(&bytes, 3, ReplayNetworkAttributeTagV1::Int, context(rl223)),
        "unsupported-k3-tag",
    );

    let mut truncated = begin_unaligned();
    truncated.push_bits(u64::from(size.min(5)), 4);
    if size <= 5 {
        truncated.push_bits(0, 1);
    }
    assert_error_category(
        decode_replay_network_k3_v1(
            &truncated.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::Location,
            context(rl223),
        ),
        "insufficient-bits",
    );
}

#[test]
fn quaternion56_invalid_and_quat48_paths_fail_closed() {
    let &code = RIGID_BODY_CODES
        .iter()
        .find(|&&value| ((value >> 15) & 1) != 0)
        .expect("need an admitted sleeping RigidBody");
    let (rl223, _, location, _, _) = rigid_fields(code);

    let mut writer = begin_unaligned();
    writer.push_bits(1, 1);
    write_vector(&mut writer, location);
    write_invalid_quat56(&mut writer);
    assert_error_category(
        decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::RigidBody,
            context(rl223),
        ),
        "invalid-k3-value",
    );

    let mut writer = begin_unaligned();
    writer.push_bits(1, 1);
    write_vector(&mut writer, location);
    writer.push_bits(0, 48);
    assert_error_category(
        decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::RigidBody,
            context(rl223),
        ),
        "insufficient-bits",
    );
}

#[test]
fn sleeping_rigid_body_never_consumes_velocity_shaped_trailing_bits() {
    let &code = RIGID_BODY_CODES
        .iter()
        .find(|&&value| ((value >> 15) & 1) != 0)
        .expect("need an admitted sleeping RigidBody");
    let (rl223, _, _, _, _) = rigid_fields(code);
    let mut writer = begin_unaligned();
    write_rigid_payload(&mut writer, code);
    let expected_end = writer.len();
    write_vector(&mut writer, 7);
    write_vector(&mut writer, 8);
    let decoded = decode_replay_network_k3_v1(
        &writer.into_bytes(),
        3,
        ReplayNetworkAttributeTagV1::RigidBody,
        context(rl223),
    )
    .expect("sleeping RigidBody must decode");
    assert_eq!(decoded.payload_end_bit, expected_end as u64);
    match decoded.value {
        ReplayNetworkK3ValueV1::RigidBody(value) => {
            assert!(value.sleeping);
            assert!(value.linear_velocity.is_none());
            assert!(value.angular_velocity.is_none());
        }
        other => panic!("unexpected variant: {other:?}"),
    }
}

#[test]
fn boost_false_context_and_pickup_truncation_are_rejected() {
    let mut writer = begin_unaligned();
    for value in [1u64, 2, 3, 4] {
        writer.push_bits(value, 8);
    }
    assert_error_category(
        decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::ReplicatedBoost,
            context(false),
        ),
        "unadmitted-k3-shape",
    );

    let mut writer = begin_unaligned();
    writer.push_bits(1, 1);
    writer.push_bits(7, 31);
    assert_error_category(
        decode_replay_network_k3_v1(
            &writer.into_bytes(),
            3,
            ReplayNetworkAttributeTagV1::PickupNew,
            context(true),
        ),
        "insufficient-bits",
    );
}

#[test]
fn exact_one_value_end_leaves_trailing_bits_unconsumed() {
    let mut writer = begin_unaligned();
    for value in [11u64, 22, 33, 44] {
        writer.push_bits(value, 8);
    }
    let expected_end = writer.len();
    writer.push_bits(0x1fff, 13);
    let decoded = decode_replay_network_k3_v1(
        &writer.into_bytes(),
        3,
        ReplayNetworkAttributeTagV1::ReplicatedBoost,
        context(true),
    )
    .expect("ReplicatedBoost must decode");
    assert_eq!(decoded.payload_end_bit, expected_end as u64);
    assert_eq!(decoded.payload_width, 32);
}
