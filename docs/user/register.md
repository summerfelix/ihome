### 注册接口


#### request请求

 	POST /user/register/

##### params参数：

	moblie str 电话号码

	password  str  密码

	password2 str 确认密码

#### response响应

##### 失败响应：

    REGISTER_ERROR_CODE_ERROR = {'code': 1001, 'msg': '验证码有误'}
    
    REGISTER_ERROR_PASSWORD_DIFFER = {'code': 1002, 'msg': '密码不一致'}
    
    REGISTER_ERROR_INFO_IS_NULL = {'code': 1003, 'msg': '请填写完整信息'}
    
    REGISTER_ERROR_USER_IS_EXIST = {'code': 1004, 'msg': '用户已存在'}