import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

// 你可以认为 state 是 store 的数据 (data)，
// getters 是 store 的计算属性 (computed)，而 actions 则是方法 (methods)。
export const useSelectClassStore = defineStore('selectClassStore', () => {

  // const selectTags = reactive(['Class2']);
  const selectTags = ref(['Class1','Class2','Class3','Class4']); // 选择框中的班级
  const selectState = ref(false) // 选择框选择状态
  const currentClass = ref('Class2') // 当前展示的班级
  const studentList = ref([]) // selectTags对应的嵌套学生列表
  const selectStudents = ref([]) // 同上，但是是选中的学生 or 学生id一维数组

  function resetSelectTags() {
    selectTags.value = []
    selectState.value = false
    console.log('resetSelectTags')
  }

  function selectStart() {
    selectState.value = false
    console.log('selectStart')
  }
  function selectEnd() {
    selectState.value = true
    console.log('selectEnd:', selectTags.value)
  }
  function switchClass(classname) {
    currentClass.value = classname
    console.log('switchClass:', currentClass.value)
  }
  function updateStudentList(list) {
    studentList.value = list
    // console.log('updateStudentList:', studentList.value)
  }
  function updateStudentListByIndex(list, index) {
    studentList.value[index] = list
    console.log('updateStudentListByIndex:', studentList.value[index])
  }
  function addSelectStudent(s_id, index) {
    // if (selectStudents.value[index]) {
    //   selectStudents.value[index].push(s_id)
    // } else {
    //   selectStudents.value[index] = [s_id]
    // }
    selectStudents.value.push(s_id)
    console.log('addSelectStudent:', selectStudents.value)
  }
  function removeSelectStudent(s_id, index) {
    // selectStudents.value = selectStudents.value[index].filter(item => item !== s_id)
    selectStudents.value = selectStudents.value.filter(item => item !== s_id)
    console.log('removeSelectStudent:', selectStudents.value)
  }
  function resetSelectStudents() {// 不设置删除一个班级的选中学生的方法，而是在选择在selectTags变化时，重新获取学生列表，重置所有选中学生
    selectStudents.value = []
    console.log('resetSelectStudents')
  } 

  return { selectTags, selectState, currentClass, studentList, selectStudents,
    updateStudentList,switchClass,updateStudentListByIndex, addSelectStudent, removeSelectStudent,resetSelectStudents,
    resetSelectTags, selectStart, selectEnd,
  }
})