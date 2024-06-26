// 向外暴露一些基本配置，比如，颜色，图标等等
export const symbolType = ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'];
export const colorConfig = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'];
export function chartIsExist (chartList, chartid) {
    for (let i = 0; i < chartList.length; i++) {
        if (chartList[i].id === chartid) {
            return true
        }
    }
    return false
}