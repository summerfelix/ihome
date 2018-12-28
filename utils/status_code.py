SUCCESS = {'code': 200, 'msg': '请求成功'}
REGISTER_ERROR_CODE_ERROR = {'code': 1001, 'msg': '验证码有误'}
REGISTER_ERROR_PASSWORD_DIFFER = {'code': 1002, 'msg': '密码不一致'}
REGISTER_ERROR_INFO_IS_NULL = {'code': 1003, 'msg': '请填写完整信息'}
REGISTER_ERROR_USER_IS_EXIST = {'code': 1004, 'msg': '用户已存在'}

LOGIN_ERROR_USER_OR_PASSWORD_ERROR = {'code': 1005, 'msg': '用户名或密码错误'}
LOGIN_ERROR_INFO_IS_NULL = {'code': 1006, 'msg': '请填写完整信息'}

UPDATE_NAME_ERROR_IS_EXIST = {'code': 1007, 'msg': '用户名已存在'}

AUTH_STATUS_IS_AUTH = {'code': 1008, 'msg': '已实名认证'}
AUTH_STATUS_NOT_AUTH = {'code': 1009, 'msg': '未实名认证'}

AUTH_ERROR_INFO_IS_NULL = {'code': 1010, 'msg': '请将信息填写完整'}
AUTH_ERROR_ID_CARD_ERROR = {'code': 1011, 'msg': '身份证号码错误'}

HOUSE_ERROR_INFO_IS_NULL = {'code': 1012, 'msg': '请将信息填写完整'}

LOGIN_STATUS_IS_LOGIN = {'code': 1013, 'msg': '用户已登录'}
LOGIN_STATUS_NOT_LOGIN = {'code': 1014, 'msg': '用户未登录'}

SEARCH_STATUS_IS_NOT_FIND = {'code': 1015, 'msg': '没有匹配结果'}

BOOKING_STATUS_DATE_ERROR = {'code': 1016, 'msg': '日期填写有误'}

BOOKING_STATUS_MAX_DAYS_ERROR = {'code': 1017, 'msg': '预定天数超过限住天数'}

ORDER_STATUS_NOT_FOUND = {'code': 1018, 'msg': '没订单'}

LORDER_STATUS_NOT_FOUND = {'code': 1019, 'msg': '没订单'}
