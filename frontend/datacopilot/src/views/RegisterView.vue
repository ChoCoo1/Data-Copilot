<template>
<!--  布局 -->
  <div style="overflow: auto">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          :ellipsis="false"
        >
          <img style="height: 100%" src="@/assets/DataCopilot.svg" alt="DataCopilot" fit="fill" />
          <el-menu-item index="0" @click="goToHome"><el-icon :size="20" color="#000000"><House /></el-icon>主页</el-menu-item>
          <el-menu-item index="1" @click="goToDatabase"><el-icon :size="20" color="#000000"><Coin /></el-icon>数据库</el-menu-item>
          <el-menu-item index="2" @click="goToQuery"><el-icon :size="20" color="#000000"><Search /></el-icon>查询</el-menu-item>
          <div class="flex-grow" />
          <el-menu-item index="3" @click="goToLogin"><el-icon :size="20" color="#000000"><UserFilled /></el-icon>登陆</el-menu-item>
          <el-menu-item index="4" @click="goToRegister"><el-icon :size="20" color="#000000"><User /></el-icon>注册</el-menu-item>
        </el-menu>
      </el-header>

<!--      页面主要部分  -->
      <el-main>
        <el-card>
          <img src="@/assets/DataCopilot.svg" alt="DataCopilot" style="height: 130px;text-align: center" />
          <el-divider style="margin: 20px 0 50px 0" > 请先注册一个账号</el-divider>
            <el-form label-width="auto">
                <el-form-item label="账号" style="margin: 20px 0 30px 0">
                  <el-input  v-model="inputUserName" placeholder="请输入账号"/>
                </el-form-item>
                <el-form-item label="密码" style="margin: 40px 0 40px 0">
                  <el-input
                    v-model="inputPwd"
                    type="password"
                    placeholder="请输入密码"
                    show-password
                  />
                </el-form-item>
                <el-form-item label="确认密码" style="margin: 40px 0 40px 0">
                  <el-input
                    v-model="inputPwdAgain"
                    type="password"
                    placeholder="请再次输入密码"
                    show-password
                  />
                </el-form-item>
                <el-form-item label="手机号" style="margin: 40px 0 40px 0">
                  <el-input
                    v-model="inputPhone"
                    placeholder="请输入手机号"
                  />
                </el-form-item>

              </el-form>
            <el-button type="primary" @click="register">注册</el-button>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import axios from 'axios'
export default {
  data() {
    return {
      activeIndex: '4', // 默认激活的菜单项
      inputUserName: '',
      inputPwd: '',
      inputPwdAgain:'',
      inputPhone: ''
    }
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    goToLogin() {
      this.$router.push('/login');
    },
    goToRegister() {
      this.$router.push('/register');
    },
    goToDatabase() {
      this.$router.push('/database');
    },
    goToQuery() {
      this.$router.push('/query');
    },
    register() {
      // 验证输入是否为空
      if (!this.inputUserName || !this.inputPwd || !this.inputPwdAgain || !this.inputPhone) {
        ElMessage.error('所有字段都是必填项，请填写完整');
        return;
      }

      // 验证两次输入的密码是否一致
      if (this.inputPwd !== this.inputPwdAgain) {
        ElMessage.error('两次输入的密码不一致');
        return;
      }

      // 构造注册请求的数据对象
      const requestData = {
        username: this.inputUserName,
        password: this.inputPwd,
        phone: this.inputPhone
      };

      // 发送注册请求
      axios.post('http://127.0.0.1:8000/api/register/', requestData)
        .then(response => {
          // 处理注册成功的响应
          ElMessage.success('注册成功');
          this.goToLogin()
          // 可以在这里做一些跳转或提示等操作
        })
        .catch(error => {
          // 处理注册失败的响应
          ElMessage.error('注册失败: ' + error.response.data);
          // 可以在这里做一些错误提示等操作
        });
    }
  }
}
</script>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
.el-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 使用视口高度作为容器的最小高度 */
}

.el-header {
  flex: 0 1 auto; /* 不占据多余空间，只占据自身所需空间 */
}
.el-main {
  display: flex;
  flex: 1; /* main元素占据剩余空间 */
  overflow: auto; /* 如果内容超出，显示滚动条 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  background: linear-gradient(-40deg,#FFDF58, #CD6CE7, #F7D7A7);
  background-size: 1000% 1000%;
  animation: gradientBG 5s ease infinite;
}

.el-card {
  display: flex; /* 添加Flexbox布局 */
  flex-direction: column; /* 使子元素垂直排列 */
  align-items: center; /* 水平居中子元素 */
  max-width: 600px;
  margin: auto;
  border-radius: 10px;
  padding: 10px;
}
.el-button{
  width: 100%
}
@keyframes gradientBG {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
  }
</style>