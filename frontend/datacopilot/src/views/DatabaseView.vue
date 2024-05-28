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
          <el-menu-item index="0" @click="goToHome"><el-icon :size="20" color="#000000"><House/></el-icon>主页</el-menu-item>
          <el-menu-item index="1" @click="goToDatabase"><el-icon :size="20" color="#000000"><Coin/></el-icon>数据库</el-menu-item>
          <el-menu-item index="2" @click="goToQuery"><el-icon :size="20" color="#000000"><Search/></el-icon>查询</el-menu-item>
          <div class="flex-grow" />
          <el-menu-item v-if="!username" index="3" @click="goToLogin" ref="ref2"><el-icon :size="20" color="#000000" ><UserFilled /></el-icon>登陆</el-menu-item>
          <el-menu-item v-if="!username" index="4" @click="goToRegister" ref="ref1"><el-icon :size="20" color="#000000" ><User /></el-icon>注册</el-menu-item>
          <el-menu-item v-if="username" index="5" ><el-icon :size="20" color="#000000" ><UserFilled /></el-icon>{{username}}</el-menu-item>
          <el-menu-item v-if="username" index="6" @click="logout" ref="ref6"><el-icon :size="20" color="#000000" ><SwitchButton /></el-icon>退出</el-menu-item>
        </el-menu>
      </el-header>

<!--      页面主要部分  -->
      <el-main>
        <el-card>
          <div class="form-container">
            <div style="margin: 0 0 20px 0;padding: 0"><el-text style="font-size: 1.6rem;color: #000000"><b>导入数据库</b></el-text></div>
            <el-divider style="width: 550px;margin: 0 0 20px 0;"></el-divider>
          <el-form label-width="auto">
              <el-form-item label="数据库类型">
                <el-select v-model="SqlType"  placeholder="请选择数据库类型">
                    <el-option label="Mysql" value="mysql" />
                </el-select>
              </el-form-item>
              <el-form-item label="主机地址">
                <el-input v-model="SqlAddress" placeholder="请输入主机号" />
              </el-form-item>
              <el-form-item label="端口号">
                <el-input v-model="SqlPort"  placeholder="请输入端口" />
              </el-form-item>
              <el-form-item label="用户名">
                <el-input v-model="SqlLoginName" placeholder="请输入数据库用户名" />
              </el-form-item>
              <el-form-item label="密码">
                <el-input v-model="SqlPwd" placeholder="请输入数据密码" />
              </el-form-item>
              <el-form-item label="数据库名称">
                <el-input v-model="SqlName" placeholder="请输入数据库名称" />
              </el-form-item>
          </el-form>
          </div>
          <div style="text-align: center">
            <el-button type="primary" @click="testConnect">验证连接</el-button>
            <el-button type="primary" @click="goToDatabase" :disabled="passConnect">导入</el-button>
          </div>
        </el-card>

        <el-card v-if="haveSql">
          <div class="form-container">
            <div style="margin: 0 0 20px 0;padding: 0"><el-text style="font-size: 1.6rem;color: #000000"><b>已导入的数据库</b></el-text></div>
            <div style="margin: 0 0 20px 0;padding: 0"><el-divider></el-divider></div>
            <el-collapse v-model="activeNames" style="width: 550px">
              <el-collapse-item :title=SqlName name="1">
                <div class="intro">数据库类型：{{SqlType}}</div>
                <div class="intro">数据库地址：{{SqlAddress}}</div>
                <div class="intro">数据库端口：{{SqlPort}}</div>
                <div class="intro">用户名：{{SqlAddress}}</div>
                <el-popconfirm title="你确定要删除数据库吗">
                  <template #reference>
                  <el-button class="intro" type="danger"><el-icon><CloseBold /></el-icon>删除数据库</el-button>
                  </template>
                </el-popconfirm>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: '1', // 默认激活的菜单项
      SqlType: '',
      SqlName: '',
      SqlPort: '',
      SqlAddress: '',
      SqlLoginName: '',
      SqlPwd: '',
      passConnect:'',
      activeNames: '0',
      haveSql: false,
      username: this.$route.query.username || '',
    }
  },
  created() {
    this.username = this.$route.query.username;
  },
  methods: {
    goToHome() {
      this.$router.push({ path: '/', query: { username: this.username } });
    },
    goToLogin() {
      this.$router.push('/login');
    },
    goToRegister() {
      this.$router.push('/register');
    },
    goToDatabase() {
      this.$router.push({ path: '/database', query: { username: this.username } });
    },
    goToQuery() {
      this.$router.push({ path: '/query', query: { username: this.username } });
    },
    logout() {
      this.username='';
    },
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
  flex-direction: column;
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
  width: 700px;
  margin:50px auto 50px auto;
  border-radius: 10px;
  padding: 10px;
}
.el-form-item {
  width: 550px;
  align-content: center;

}
.form {
  max-width: 600px; /* 最大宽度，根据实际需要调整 */
  width: 100%; /* 让表单宽度自适应 */
}
.form-container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  text-align: center; /* 确保内部元素也居中，如果需要 */
  padding: 20px; /* 根据需要添加内边距 */
}
.el-divider {
  margin: 10px auto; /* 调整上边距和下边距 */
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
.intro{
  margin:0;
  padding: 5px;
}
</style>