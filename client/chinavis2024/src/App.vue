<script setup>
// import { RouterLink, RouterView } from 'vue-router'
import LeftClassBar from './components/LeftClassBar.vue';
import ParallelChart from './components/ParallelChart.vue';
import KnowledgeSunburst from './components/KnowledgeSunburst.vue';
import LearnHeatMap from './components/LearnHeatMap.vue';
import RadarChart from './components/RadarChart.vue';
import StateChart from './components/StateChart.vue';
import TSNEScatter from './components/TSNEScatter.vue';
import DayActivityRiver from './components/DayActivityRiver.vue';
import MultiLineChart from './components/MultiLineChart.vue';
</script>

<!-- <template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->
<template>
  <div class="header">
    <p>Visualization Challenge 1.1 of Chinavis 2024</p>
  </div>
  <div class="main">
    <div class="sub-main left" style="width: 30%; height: 100%">
      <div class="container">
        <div id="parallelchart">
          <ParallelChart />
        </div>
        <div style="width: 100%; height: 30%;">
          <LeftClassBar />
        </div>
        <div id="weak-knowledge">
          <!-- <WordCloud /> -->
          <div style="width: 65%; height: 100%;"> 
            <KnowledgeSunburst />
          </div>
          <div id="statechart" style="width: 35%; height: 100%;">
            <StateChart />
          </div>
        </div>
        <div id="heatmap">
          <LearnHeatMap />
        </div>
      </div>
    </div>
    <div class="sub-main mid" style="width: 40%; height: 100%">
      <div class="container">
        <div id="radarchart" style="width: 100%; height: 50%;">
            <RadarChart />
        </div>
        <div id="activity" style="width: 100%; height: 25%;">
            <DayActivityRiver />
        </div>
        <div id="attemps-correct" style="width: 100%; height: 25%;">
            <MultiLineChart />
        </div>
        
      </div>
    </div>
    <div class="sub-main right" style="width: 30%; height: 100%">
      <div class="container">
          <div style="width: 100%; height: 30%;">
            <TSNEScatter />
          </div>
      </div>
    </div>
    <div id="tooltip" class="prompt-hide"></div>
  </div>

</template>

<style scoped>
.header {
  width: 100%;
  height: 4%;
  background-color: black;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.main {
  height: 96%;
  width: 100%;
  /* background-color: aquamarine; */
  display: flex;
}
.sub-main {
  padding: 5px;
}
.container {
  width: 100%;
  height: 100%;
  padding: 5px;
  display: flex;
  flex-direction: column;
}
#parallelchart {
  height: 25%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
#weak-knowledge{
  height: 25%;
  width: 100%;
  display: flex;
}
#heatmap{
  height: 20%;
  width: 100%;
}
.paper-list-outer{
  width: 100%;
  height: 30%;
  /* padding-left: 5px; */
  padding-bottom: 5px;
}
.author-list-outer{
  width: 100%;
  height: 20%;
}
</style>

