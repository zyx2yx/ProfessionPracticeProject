import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useStudentStore = defineStore('student', () => {
  const totalSelectStudent = ref({}) // 选择框中的学生
  const lastSelectStudent = ref([]) // 上次选择的学生
  const lastSelectCluster = ref(0) // 上次选择的聚类

  function updateTotalSelectStudent(cluster, student) {
    console.log('updateTotalSelectStudent:', cluster, student);
    // console.log('totalSelectStudent:', totalSelectStudent.value);
    
    totalSelectStudent.value[cluster] = student
  }

  function updateLastSelectStudent(student) {
    console.log('updateLastSelectStudent:', student);
    
    lastSelectStudent.value = student
  }

  function updateLastSelectCluster(cluster) {
    console.log('updateLastSelectCluster:', cluster);
    
    lastSelectCluster.value = cluster
  }

  // const doubleCount = computed(() => count.value * 2)
  // function increment() {
  //   count.value++
  // }

  return { totalSelectStudent, lastSelectStudent, lastSelectCluster, 
    updateTotalSelectStudent, updateLastSelectStudent, updateLastSelectCluster }
})
