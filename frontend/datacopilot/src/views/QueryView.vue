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
          <img style="height: 100%" src="@/assets/DataCopilot.svg" alt="DataCopilot" />
          <el-menu-item index="0" @click="goToHome"><el-icon :size="20" color="#000000"><House /></el-icon>主页</el-menu-item>
          <el-menu-item index="1" @click="goToDatabase"><el-icon :size="20" color="#000000"><Coin /></el-icon>数据库</el-menu-item>
          <el-menu-item index="2" @click="goToQuery"><el-icon :size="20" color="#000000"><Search /></el-icon>查询</el-menu-item>
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

<!--        搜索框-->
        <div class="search-container">
          <el-select v-model="searchSqlName" placeholder="请选择数据库" style="width: 150px;margin:0;padding-right: 10px">
            <el-option
              v-for="item in searchTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-input
              v-model="searchQuery"
              class="search-input"
              placeholder="请输入您想搜索的内容"
              @input="fetchSearchHistory"
            >
            <template #prepend>
              <el-icon :size="20" color="#000000"><Search /></el-icon>

            </template>
            <template #suffix>
                <el-button class="roundBtn" @click="searchSql"><el-icon :size="20" color="#FFFFFF" ><Bottom/></el-icon></el-button>
            </template>
          </el-input>
        </div>

        <!-- 显示SQL结果 -->
          <el-card v-if="displaySql" style="height: auto;" >
            <el-text style="margin: 0 auto;font-size: 1.8rem;color: black"><b>以下是生成结果</b></el-text>
            <el-divider style="width: 900px"></el-divider>
            <!-- 回复框  -->
            <el-card class="chatBox" v-loading="waitSql" style="width: 900px;height: auto">
              <div style="display: flex; justify-content: space-between; width: 800px; margin: 0 auto; padding: 0;">
                <el-text style="text-align: left; width: 300px;color: black"><b>SQL语句</b></el-text>
                <el-button type="text" style="color: black;" @click="copySql">
                  <el-icon :size="18"><CopyDocument /></el-icon> 复制结果
                </el-button>
              </div>
              <el-divider style="width: 100%;margin: 10px auto"></el-divider>
              <el-text style="margin: 10px auto;font-size: 1.2rem;color: black">{{this.sqlResult}}</el-text>
            </el-card>
<!--       数据展示SQL查询结果 -->
            <el-text style="margin:30px auto;padding: 20px;font-size: 1.4rem;color: black"><b>SQL语句执行结果</b></el-text>
            <el-divider style="width: 900px"></el-divider>
            <el-table v-loading="waitSql" :data="tableData" height="400" :max-height="1000" style="width: 900px;margin:20px auto;">
               <el-table-column v-for="column in columns" :key="column" :prop="column" :label="column" />
            </el-table>
            <div v-if="shouldChart">
              <el-select v-model="chartType" placeholder="请选择图表类型" style="width: 150px;margin:0;padding-right: 10px">
                <el-option
                  v-for="item in chartTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
              <el-button @click="showChart"> 可视化该图表</el-button>
            </div>
          </el-card>

            <!-- 可视化图表  -->
            <el-card v-if="displayChart" style="max-height: 1000px" v-loading="waitChart">
              <el-text style="margin: 0;font-size: 1.8rem;color: black"><b>可视化结果</b></el-text>
              <el-divider style="width: 900px"></el-divider>
              <div ref="chartContainer" style="width: 900px; height: 400px;"></div>
              <el-button @click="saveChart" :disabled="waitChart"> 保存图表</el-button>
          </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from 'echarts';
import {ElMessage} from "element-plus";
export default {
  data() {
    return {
      activeIndex: '2', // 默认激活的菜单项
      searchQuery: '',
      displaySql: false,
      displayChart: false,
      shouldChart: false,
      waitSql: false,
      waitChart: false,
      sqlResult: '',
      username: this.$route.query.username || '',
      tableData : [],
      columns: [],
      searchTypeOptions: [],
      searchSqlName:'',
      chartType: '',
      chartTypeOptions: [
        { value: 'bar', label: '柱状图' },
        { value: 'line', label: '折线图' },
      ]
    }
  },
  created() {
    this.fetchDatabaseConnections();
  },
  methods: {
    goToHome() {
      this.$router.push({path: '/', query: {username: this.username}});
    },
    goToLogin() {
      this.$router.push('/login');
    },
    goToRegister() {
      this.$router.push('/register');
    },
    goToDatabase() {
      this.$router.push({path: '/database', query: {username: this.username}});
    },
    goToQuery() {
      this.$router.push({path: '/query', query: {username: this.username}});
    },
    goToUser() {
      this.$router.push({path: '/user', query: {username: this.username}});
    },
    showChart() {
      this.displayChart = true; // 显示图表
      this.waitChart = true; // 加载图表时显示加载状态

      // 根据用户选择的图表类型执行相应的逻辑
      this.$nextTick(() => {
        if (this.chartType === 'bar') {
          // 生成柱状图
          this.generateBarChart();
        } else if (this.chartType === 'line') {
          // 生成折线图
          this.generateLineChart();
        } else {
          // 其他类型的图表逻辑
          this.$message.error('请选择正确的图表类型');
        }
        this.waitChart = false; // 停止加载状态
      });
    },
    generateBarChart() {
      // 获取第一列和最后一列的数据
      const xData = this.tableData.map(item => item[this.columns[0]]);
      const yData = this.tableData.map(item => item[this.columns[this.columns.length - 1]]);

      // 使用 ECharts 生成柱状图
      const chart = echarts.init(this.$refs.chartContainer);
      const option = {
        title: {
          text: '柱状图展示'
        },
        tooltip: {},
        xAxis: {
          name: this.columns[0],
          data: xData,
        },
        yAxis: {
          name: this.columns[this.columns.length - 1],
          type: 'value',
        },
        series: [{
          name: this.columns[this.columns.length - 1],
          type: 'bar',
          data: yData
        }]
      };
      chart.setOption(option);
    },
    generateLineChart() {
      // 获取第一列和最后一列的数据
      const xData = this.tableData.map(item => item[this.columns[0]]);
      const yData = this.tableData.map(item => item[this.columns[this.columns.length - 1]]);

      // 使用 ECharts 生成折线图
      const chart = echarts.init(this.$refs.chartContainer);
      const option = {
        title: {
          text: '折线图展示'
        },
        tooltip: {},
        xAxis: {
          data: xData,
          name: this.columns[0],
        },
        yAxis: {
          name: this.columns[this.columns.length - 1],
        },
        series: [{
          name: this.columns[this.columns.length - 1],
          type: 'line',
          data: yData
        }]
      };
      chart.setOption(option);
    },
    copySql() {
      // 复制 SQL 查询结果到剪贴板
      if(this.sqlResult===''){
        this.$message.error('请先执行SQL查询');
      }else{
      navigator.clipboard.writeText(this.sqlResult)
        .then(() => {
          this.$message.success('复制成功');
        })
        .catch((err) => {
          console.error('复制失败：', err);
          this.$message.error('复制失败，请手动复制');
        })};
    },
    saveChart() {
      // 获取图表实例
      const chartInstance = echarts.getInstanceByDom(this.$refs.chartContainer);
      // 导出为图片
      chartInstance.convertToPixel('cartesian2d', [0, 0]);
      const base64 = chartInstance.getDataURL({type: 'png', pixelRatio: 2});
      // 创建一个a标签，模拟点击下载
      const link = document.createElement('a');
      link.href = base64;
      link.download = 'chart.png';
      link.click();
    },
    fetchDatabaseConnections() {
      axios.get('http://127.0.0.1:8000/api/get_database_name', {
        params: {
          username: this.username // 替换为实际用户名
        }
      })
      .then(response => {
        // 将返回的数据填充到 searchTypeOptions 中
        this.searchTypeOptions = response.data.map(connection => ({
          value: connection.sql_name,
          label: connection.sql_name
        }));
      })
      .catch(error => {
        console.error('Error fetching database connections:', error);
      });
    },
    searchSql() {
      if (this.searchQuery === '') {
        this.$message.error('请输入搜索内容');
      }
      else if (this.searchSqlName===''){
        this.$message.error('请选择数据库');
      }
      else {
        this.waitSql = true;
        this.displaySql = true;
        this.sqlResult = '';
        this.tableData = [];
        this.columns = [];
        // 发送搜索内容到后端
        let RequestData = {
          username: this.username,
          search_query: this.searchQuery,
          sql_name: this.searchSqlName,
        }
        axios.post('http://127.0.0.1:8000/api/generate_sql_query/', RequestData)
          .then(response => {
            // 将后端返回的 SQL 查询语句保存到数据中
            this.sqlResult = response.data.sql_query;
            this.columns = response.data.columns;
            this.tableData = response.data.results;
            this.shouldChart = response.data.shouldChart;
            this.waitSql = false;
            this.waitExec = false;
            this.$message.success('搜索成功');
            this.addSearchHistory();
          })
          .catch(error => {
            this.waitSql = false;
          });
      }
    },addSearchHistory() {
        let requestData = {
          username: this.username,
          search_query: this.searchQuery,
          search_sql_name: this.searchSqlName,
        };
        axios.post('http://127.0.0.1:8000/api/add_search_history/', requestData)
          .then(response => {
            // 成功保存搜索历史
            console.log('成功导入搜索历史');
          })
          .catch(error => {
            console.log('引入搜索历史失败');
          });
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
  text-align: center;
  width: 1000px;
  margin:50px auto 50px auto;
  border-radius: 10px;
  padding: 10px;
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
.search-container{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin:50px auto 50px auto;
}
.search-input {
  width: 550px; /* 根据需要调整宽度 */
  height: 40px;
}
.roundBtn{
width: 30px;
height: 30px;
border-radius:50%;
background-color:#000000;
border:0;
}
.chatBox {
  width: 550px;
  max-height: 400px; /* 限制聊天框的最大高度 */
  overflow: auto;
  margin: 20px auto;
  padding: 0;
  background-color: #f9f9f9;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
}
</style>