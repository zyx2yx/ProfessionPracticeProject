<script setup>
import * as d3 from "d3";
import { onMounted, reactive, ref, watch, onUpdated } from "vue";
import { storeToRefs } from "pinia";
import { UserOutlined, UsergroupAddOutlined } from '@ant-design/icons-vue';


import { useSelectClassStore } from "../stores/selectClass";
import { reqGetClassStudentList, reqStuFuzzySearch } from '../api/index'
// import { useSelectParentFieldStore } from "../stores/selectParentField";

// import data from "../data/OverView/data.json";

// 你可以直接从 store 中解构 action
const { resetSelectTags, selectStart, selectEnd, switchClass, updateStudentList, updateStudentListByIndex, addSelectStudent, resetSelectStudents } = useSelectClassStore();
// 为了从 store 中提取属性时保持其响应性，你需要使用 storeToRefs()
const { selectTags, currentClass, studentList, selectStudents } = storeToRefs(useSelectClassStore())
// ref返回一个包含value属性的对象，通过修改value属性的值，可以触发组件更新。
// 而reactive返回一个响应式的Proxy对象。，通过修改该对象的属性值，可以触发组件更新。

// 请注意，所有store仓库 是一个用 reactive 包装的对象，这意味着不需要在取值时 后面写 .value。
// 就像 setup 中的 props 一样，我们也不能对它进行解构：对 store 的解构会破坏响应性。

// 在模板中访问 store 的属性时，不管是ref还是reactive，都不需要在属性后面加 .value。

// const store = useCounterStore()
// ❌ 这将不起作用，因为它破坏了响应性
// 这就和直接解构 `props` 一样
// const { name, doubleCount } = store
// name // 将始终是 "Eduardo"
// doubleCount // 将始终是 0
// setTimeout(() => {
//   store.increment()
// }, 1000)
// ✅ 这样写是响应式的
// 💡 当然你也可以直接使用 `store.doubleCount`
// const doubleValue = computed(() => store.doubleCount)

/*  ....................some global variable or config.......................  */

let width;
let height;
let length;
let radius;
let promptBox = d3.select("#tooltip");
let body = d3.select("body");
let preShowingCart
let preshowingTitle
let preSearchColumn

const boxStyle = {
  width: '100%',
  borderRadius: '6px',
  justifyContent: 'space-between',
  alignItems: 'center',
};


const tagsData = ['AllClass', 'Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6'
, 'Class7', 'Class8', 'Class9', 'Class10', 'Class11', 'Class12', 'Class13', 'Class14', 'Class15'
]

/*  ......................some global variable or config............................  */

/*..........................methods................................*/ 

// 输入框选择班级
const handleChange = value => {
  console.log(`selected ${value}`); // value 为[]
  // console.log(value)
  // 发送请求获取班级学生列表
  reqStudenListByClassid(value)
  resetSelectStudents();
  switchClass(value[0])
};
const handleResetSelect = () => {
  resetSelectTags();
  resetSelectStudents();
};
const handleFocus = () => {
  selectStart();
};
const handleCommit = () => {
  selectEnd();
};
// 点击班级标签
const handleTabClick = (e) => {// 点击班级标签
  // console.log(e.target.innerText)
  switchClass(e.target.innerText)
  preShowingCart && preShowingCart.classed('show-card',false)
  // preShowingCart =  d3.select(e.currentTarget)
  preShowingCart =  d3.select('#left-class-bar')
      .select(`#${currentClass.value}`)
      .classed('show-card',true)
  // console.log("currentClass.value:",currentClass.value)

  preshowingTitle && preshowingTitle.classed('tab-item-show',false)
  preshowingTitle = d3.select(e.currentTarget)
      // .select('.tab-item')
      .classed('tab-item-show',true)
}
const handlemovein = (e) => {
  // e.currentTarget.style.backgroundColor = '#eaf4ff'
  d3.select(e.currentTarget).classed('user-hover',true)
}
const handlemoveout = (e) => {
  // e.currentTarget.style.backgroundColor = 'white'
  d3.select(e.currentTarget).classed('user-hover',false)
}
const handleRowClick = (e) => {
  // console.log(e.currentTarget)
  // console.log(e.currentTarget.classList)
  d3.select(e.currentTarget).classed('stu-selected',true)
  let class_idx = selectTags.value.indexOf(currentClass.value)
  addSelectStudent(studentList.value[class_idx][e.currentTarget.getAttribute('idx')].student_ID, class_idx)
}

const reqStudenListByClassid = async (class_list) => {
  let student_list = await reqGetClassStudentList(class_list)
  console.log(student_list);
  updateStudentList(student_list.res_data)

}

function init(){
  // 默认展开默认选择的班级
  let firstPaperCard = d3.select(`#left-class-bar #${currentClass.value}`)
  // let firstPaperCard = d3.select(`#left-class-bar .table-block`)
  // console.log("firstPaperCard:",firstPaperCard,"currentClass.value:",currentClass.value,"d3.select():",d3.select('.class-tab-list > .table-block'));
  preShowingCart && preShowingCart.classed('show-card',false)
  preShowingCart = firstPaperCard && firstPaperCard.classed('show-card',true)

  // let firstPaperTitle = d3.select('#left-class-bar .tab-item')
  let firstPaperTitle = d3.select(`#left-class-bar #tab${currentClass.value}`)
  preshowingTitle && preshowingTitle.classed('tab-item-show',false)
  preshowingTitle = firstPaperTitle && firstPaperTitle.classed('tab-item-show',true)
}
// 模糊搜索框
const fuzzyValue = ref('');
let tempStuListByIdx = [] // 保存模糊搜索前的数据
const onFuzzySearch = async searchValue => {

  // 查找currentClass.value在selectTags中的索引
    let class_idx = selectTags.value.indexOf(currentClass.value)
  if (searchValue === '') {
    if (tempStuListByIdx.length != 0) { // 此时需要恢复原始数据
      updateStudentListByIndex(tempStuListByIdx, class_idx)
      tempStuListByIdx = []
    }
  }else{
    // 发送请求获取模糊搜索结果
    let fuzzySearchRes = await reqStuFuzzySearch(currentClass.value, refSearchColumn.value, searchValue)
    // console.log("fuzzySearchRes:",fuzzySearchRes);
    
    // 将搜索结果更新到studentList中
    tempStuListByIdx = studentList.value[class_idx]
    updateStudentListByIndex(fuzzySearchRes.res_data, class_idx)
  }
};

const onFuzzySearchChange = (searchValue) => {
  // 如果搜索框为空，恢复原始数据
  // console.log("searchvalue",searchValue,tempStuListByIdx.value);
  // if (searchValue === '') {
  //   updateStudentListByIndex(tempStuListByIdx.value, selectTags.value.indexOf(currentClass.value))
  // }
};

const refSearchColumn = ref('student_ID')
// 处理表头点击事件（事件委托）
const handleTableHeadClick = (e) => {
  // console.log(e.target.innerText)
  // 为点击的元素增加class
  preSearchColumn || (preSearchColumn = d3.select('#table-head .search-column')) // 找到第一个有search-column的元素
  preSearchColumn && preSearchColumn.classed('search-column', false) // 移除上一个search-column
  preSearchColumn = d3.select(e.target).classed('search-column', true) // 为当前点击的元素增加search-column
  refSearchColumn.value = e.target.innerText
}

function clickHandler(e){
  preShowingCart && preShowingCart.classed('show-card',false)
  preShowingCart =  d3.select(e.currentTarget)
      .select('.table-block')
      .classed('show-card',true)

  // preshowingTitle && preshowingTitle.classed('tab-item-show',false)
  // preshowingTitle = d3.select(e.currentTarget)
  //     .select('.tab-item')
  //     .classed('tab-item-show',true)
}

/*..........................methods................................*/ 

   /*........vue hooks or macro definition..........*/

onMounted(async () => {
  width = document.getElementById("left-class-bar").offsetWidth;
  height = document.getElementById("left-class-bar").offsetHeight;
  length = width > height ? height : width;
  radius = length / 6;
  promptBox = d3.select("#tooltip");

  // let student_list = JSON.parse(await reqGetClassStudentList(selectTags.value)) // 获取学生列表
  let student_list = await reqGetClassStudentList(selectTags.value) // 获取学生列表
  console.log(student_list);
  // console.log(studentList.status);
  updateStudentList(student_list.res_data)

  draw();
  // init();
});

watch(studentList, (newVal, oldVal) => {
  // console.log("studentList changed:",newVal,oldVal)
  // draw();
  // init();
})
onUpdated(() => {
  console.log("studentList updated")
  // draw();
  init();// 不在onMounted、watch中调用init()，因为此时DOM还未挂载表格
  // 在学生信息列表更新后，首先DOM更新，然后调用init()，通过CSS display控制表格的显示，该参数会使DOM发生变化
  // 会再次触发onUpdated，调用init()，但此时不会再次触发DOM更新，显示的班级DOM元素不会变化
  // 2024.6.13 模糊查询输入框为受控组件，onUpdated会频繁触发
})

   /*........vue hooks or macro definition..........*/

function addEvent(selection) {
  selection
    .on("mouseover.over", function (event, d) {
      let [posX, posY] = d3.pointer(event, body);
      promptBox
        .attr("class", "prompt-show")
        .style("top", posY - 50 + "px")
        .style("left", posX + 15 + "px")
        .html(
          `${d.data.name}:${d.value}<br>${(
            (d.value * 100) /
            d.parent.value
          ).toFixed(2)}%`
        );
    })
    .on("mousemove", function (event) {
      let [posX, posY] = d3.pointer(event, body);
      promptBox.style("top", posY - 50 + "px").style("left", posX + 15 + "px");
    })
    .on("mouseout.out", function () {
      promptBox.attr("class", "prompt-hide");
    });
}

function draw() {


}

function isInlist(list, item) {
  // 判断list是否有值
  if (!list) {
    return false;
  }
  for (let i = 0; i < list.length; i++) {
    if (list[i] === item) {
      return true;
    }
  }
  return false;
}

</script>

<template>
  <div id="left-class-bar">
    <!-- <a-flex :style="{ ...boxStyle }">选择班级:
      <a-select
      v-model:value="selectTags"
      mode="multiple"
      style="width: 60%"
      placeholder="Please select Class"
      :options="tagsData.map((_, i) => ({ value: _}))"
      @change="handleChange"
      @focus="handleFocus"
      size="small"
    ></a-select>
  
      <a-button size="small"
      @click="handleResetSelect"
      >清除</a-button>

      <a-button type="primary" size="small" @click="handleCommit">确认</a-button>
    </a-flex> -->
    <div style="display: flex; justify-content: space-between; background-color: #eaf4ff; margin: 5px 0;">
      <div style="display: flex; ">
        <div class="tab-item" v-for="classname in selectTags" :key="classname" @click="handleTabClick"
          :id="`tab${classname}`"
          >{{ classname }}
        </div>
      </div>
      <a-input-search
        v-model:value="fuzzyValue"
        placeholder="fuzzy search"
        style="width: 200px"
        size="small"
        @search="onFuzzySearch"
        @change="onFuzzySearchChange"
        allow-clear
      />
    </div>
    <div style="display: flex;flex-grow: 1; overflow: hidden; margin-bottom: 5px;">
      <div id="table-container">
        <div id="table-head" @click="handleTableHeadClick">
          <div class="cell1 search-column">student_ID</div>
          <div class="cell2">sex</div>
          <div class="cell3">age</div>
          <div class="cell4">major</div>
        </div>
        <div id="table-body">
          <!-- <div class="class-tab-list"> -->
            <div class="table-block" v-for="(s_list, index) in studentList" :id="selectTags[index]">
              <!-- <div :class="['table-row', {'stu-selected':isInlist(selectStudents[index], s.student_ID)}]" v-for="(s,i) in s_list" :key="i" :idx="i" -->
              <div :class="['table-row', {'stu-selected':isInlist(selectStudents, s.student_ID)}]" v-for="(s,i) in s_list" :key="i" :idx="i"
                @mouseover="handlemovein"
                @mouseout="handlemoveout"
                @click="handleRowClick"
                >
                <div class="cell1">{{s.student_ID}}</div>
                <div class="cell2">{{s.sex}}</div>
                <div class="cell3">{{s.age}}</div>
                <div class="cell4">{{s.major}}</div>
              </div>
            </div>
          <!-- </div> -->
        </div>
      </div>
      <div id="selected-tabs">
        <a-tag class="tabs" size="small" v-for="classid in selectTags"> <template #icon><UsergroupAddOutlined /></template>{{ classid }}</a-tag>
        <a-tag class="tabs" size="small" closable @close="stutabclose" v-for="sid in selectStudents"> <template #icon><UserOutlined /></template>{{ `${sid.slice(0, 6)}...` }}</a-tag>
      </div>
    </div>
    
  </div>
</template>

<style scoped>
#left-class-bar {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.tab-item{
  margin: 0;
  padding: 0 5px;
  /* border: 1px solid rgb(234, 234, 234); */
  /* border-radius: 10px; */
  background-color: #eaf4ff;
  cursor: pointer;
}

#table-container{
  width: 80%;
  height: 100%;
  display: flex;
  flex-direction: column;
  /* overflow: hidden; */
  /* flex-grow: 1; */
}

#table-head{
  /* position: sticky;
  top: 0;  */
  width: 100%;
  display: flex;
 /* background-color: #eaf4ff; *//*设置表头背景色*/
  background-color: white; /*设置表头背景色*/
  text-align: center;
}
#table-body {
  width: 100%;
  flex-grow: 1;
  /* height: 60%; */
  overflow-y: auto;
  /* display: flex;
  flex-direction: column; */
  text-align: center;
  /* border-width: 0 1px 1px 0; */
  border-width: 1px 0 0 1px;
  border-style: solid;
  border-color: #eaf4ff;
  -ms-overflow-style: none; /* IE 10+ */
  scrollbar-width: none; /* Firefox */
}
#selected-tabs{
  width: 20%;
  padding-left: 5px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* align-items: center; */
}
#selected-tabs .tabs{
  width: 100%;
  text-align: center;
  margin: 0;
}
#table-body::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}
.table-block{
  /* 给table设置height=0不起作用 */
  width: 100%;
  /* height: 0; */
  /* display: flex; */
  /* overflow: hidden;  */
  /* visibility: hidden; */
  display: none;
  /* flex-wrap: wrap; */
  transition: height 500ms;
  /* position: absolute; */
}
.table-row{
  display: flex;
}
.cell1{
  width: 40%;
}
.cell2{
  width: 15%;
}
.cell3{
  width: 10%;
}
.cell4{
  width: 25%;
}
.cell1,.cell2,.cell3,.cell4{
  flex-grow: 1;
  /* border-width: 1px 0 0 1px; */
  border-width: 0 1px 1px 0;
  border-style: solid;
  border-color: #edeaff;
  cursor: pointer;
}
:deep(.show-card){
  /* height: 100%; */
  /* visibility: visible; */
  display: block;
}

.tab-item-show{
  /* white-space: normal; */
  /* border-bottom: 1px solid rgb(234, 234, 234); */
  /* background-color: #eaf4ff; */
  background-color: white;
}
.search-column, .user-hover{
  /* background-color: #5da9fa; */
  /* color: rgba(0, 0, 255, 0.2); */

  /* background-color: #eaf4ff; */
  background-color: #bae0ff;
  font-weight: bold;
}
.stu-selected{
  background-color: #e6f4ff;
  /* border: 1px solid #6392b6; */
}
</style>
