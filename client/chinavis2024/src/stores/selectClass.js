import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

// 你可以认为 state 是 store 的数据 (data)，
// getters 是 store 的计算属性 (computed)，而 actions 则是方法 (methods)。
export const useSelectClassStore = defineStore('selectClassStore', () => {

  // const selectTags = reactive(['Class2']);
  const selectTags = ref(['Class2']);
  const selectState = ref(false)
  const currentClass = ref('Class2')
  const studentList = ref([]) 

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

  return { selectTags, selectState, currentClass, studentList, 
    updateStudentList,switchClass,updateStudentListByIndex,
    resetSelectTags, selectStart, selectEnd,
  }
})