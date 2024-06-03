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
          <el-menu-item v-if="username" index="5" @click="goToUser"><el-icon :size="20" color="#000000" ><UserFilled /></el-icon>{{username}}</el-menu-item>
          <el-menu-item v-if="username" index="6" @click="logout" ref="ref6"><el-icon :size="20" color="#000000" ><SwitchButton /></el-icon>退出</el-menu-item>
        </el-menu>
      </el-header>

<!--      页面主要部分  -->
      <el-main>
        <el-backtop :right="100" :bottom="100" style="color: black"/>
        <el-card>
          <div style="margin: 0 0 0px 0;padding: 0"><el-text style="font-size: 1.6rem;color: #000000"><b>修改密码</b></el-text></div>
          <el-divider style="margin: 20px 0 50px 0" > </el-divider>
            <el-form label-width="auto">
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
            </el-form>
          <el-button type="primary" @click="UpdatePassword" style="width: 300px">修改密码</el-button>
          <el-divider style="margin: 20px 0 20px 0" > </el-divider>
          <div style="margin: 0 0 0px 0;padding: 0"><el-text style="font-size: 1.6rem;color: #000000"><b>修改手机号</b></el-text></div>
              <el-form label-width="auto">
                <el-form-item label="手机号" style="margin: 40px 0 40px 0">
                  <el-input
                    v-model="inputPhone"
                    placeholder="请输入手机号"
                  />
                </el-form-item>

              </el-form>
            <el-button type="primary" @click="UpdatePhone" style="width: 300px">修改手机号</el-button>
        </el-card>

        <el-card v-if="connections.length>0">
          <div class="form-container">
            <div style="margin: 0 0 20px 0;padding: 0"><el-text style="font-size: 1.6rem;color: #000000"><b>已导入的数据库</b></el-text></div>
            <el-collapse v-model="activeNames" style="width: 550px" accordion>
              <el-collapse-item  v-for="connection in connections" :key="connection.id" :name="connection.id">
                <template #title>
                  <b style="font-size: 1.2rem">{{connection.sql_name}}</b>
                </template>
                <div class="intro">数据库类型：{{ connection.sql_type }}</div>
                <div class="intro">数据库地址：{{ connection.sql_address }}</div>
                <div class="intro">数据库端口：{{ connection.sql_port }}</div>
                <el-popconfirm title="你确定要删除数据库吗" @confirm="handleDelete(connection.id)">
                  <template #reference>
                  <el-button class="intro" type="danger"><el-icon><CloseBold /></el-icon>删除数据库</el-button>
                  </template>
                </el-popconfirm>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>

        <el-card>
          <div class="form-container">
            <div style="margin: 0 0 20px 0;padding: 0"><el-text style="font-size: 1.6rem;color: #000000"><b>搜索历史</b></el-text></div>
            <el-table :data="tableData" height="400" :max-height="1000" style="width: 700px;margin:20px auto;">
               <el-table-column v-for="column in columns" :key="column" :prop="column" :label="column" />
            </el-table>
          </div>
        </el-card>


      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      activeIndex: '5', // 默认激活的菜单项
      inputPwd: '',
      inputPwdAgain:'',
      inputPhone: '',
      username: this.$route.query.username || '',
      connections: [],
      activeNames: '0',
      columns:['搜索时间','检索数据库','搜索内容'],
      tableData: [],
    }
  },
  created() {
    this.username = this.$route.query.username;
    this.fetchDatabaseConnections();
    this.fetchSearchHistory();
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
    goToUser() {
      this.$router.push({ path: '/user', query: { username: this.username } });
    },
    logout() {
      this.username='';
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const formattedDate = date.toLocaleDateString('zh-CN');  // 获取本地日期字符串
      const formattedTime = date.toLocaleTimeString('zh-CN');  // 获取本地时间字符串
      return `${formattedDate} ${formattedTime}`;
    },
    fetchSearchHistory() {
      const RequestData = {
        params: {
          username: this.username
        }
      };
      axios.get('http://127.0.0.1:8000/api/get_search_history/', RequestData)
        .then(response => {
          this.tableData = response.data.map(item => ({
            '搜索时间': this.formatTimestamp(item.created_at),
            '检索数据库': item.search_sql_name,
            '搜索内容': item.search_query
          }));
        })
        .catch(error => {
          console.error("There was an error fetching the search history!", error);
        });
  },
    fetchDatabaseConnections() {
      const RequestData = {
          params: {
            username: this.username
          }
        };
      axios.get('http://127.0.0.1:8000/api/get_database_connections/',RequestData)
        .then(response => {
          this.connections = response.data;
        })
        .catch(error => {
          console.error("There was an error fetching the database connections!", error);
        });
    },
    handleDelete(id) {
      axios.delete(`http://127.0.0.1:8000/api/delete_database_connection/`,{data:{sql_id:id}})
        .then(response => {
          ElMessage.success("删除成功");
          this.fetchDatabaseConnections();
          // 在这里你可能想要更新前端的数据库连接列表
        })
        .catch(error => {
          ElMessage.error("删除失败")
        });
    },
    UpdatePassword() {
      if (this.inputPwd === '' || this.inputPwdAgain === ''){
        ElMessage.error("密码不能为空，请重新输入");
      }
      else if (this.inputPwd !== this.inputPwdAgain) {
        ElMessage.error("两次输入的密码不一致，请重新输入");
      }
      else {
        // 发送修改密码的请求到后端
        const requestData = {
          username: this.username,
          password: this.inputPwd
        };
        axios.post('http://127.0.0.1:8000/api/update_password/', requestData)
            .then(response => {
              ElMessage.success("密码修改成功");
              // 清空输入框
              this.inputPwd = '';
              this.inputPwdAgain = '';
            })
            .catch(error => {
              ElMessage.error("密码修改失败，请稍后重试");
              console.error("Error updating password:", error);
            });
      }
      },
    UpdatePhone() {
      if (this.inputPhone === ''){
        ElMessage.error("手机号不能为空，请重新输入");
      }
      else if (this.inputPhone.length!==11){
        ElMessage.error("手机号格式不正确，请重新输入");
      }
      else{
        // 发送修改手机号的请求到后端
        const requestData = {
          username: this.username,
          phone: this.inputPhone
        };
        axios.post('http://127.0.0.1:8000/api/update_phone/', requestData)
          .then(response => {
            ElMessage.success("手机号修改成功");
            // 清空输入框
            this.inputPhone = '';
          })
          .catch(error => {
            ElMessage.error("手机号修改失败，请稍后重试");
            console.error("Error updating phone number:", error);
          });
      }
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
  justify-content: center;
  text-align: center; /* 确保内部元素也居中，如果需要 */
  width: 800px;
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