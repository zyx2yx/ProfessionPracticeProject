<script setup>
// import { RouterLink, RouterView } from 'vue-router'
import LeftClassBar from './components/LeftClassBar.vue'
import ParallelChart from './components/ParallelChart.vue';
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
    <div class="sub-main left" style="width: 35%; height: 100%">
      <div class="container">
        <LeftClassBar />
        <div id="paper-author">
          <!-- <HighCitationPaper />
          <HighOutputAuthor /> -->
          <ParallelChart />
        </div>
        <div id="word-cloud">
          <!-- <WordCloud /> -->
        </div>
      </div>
    </div>
    <div class="sub-main mid" style="width: 60%; height: 100%">
      <div class="container">
        <!-- <ForceCahrt /><OverViewBar /> -->
      </div>
    </div>
    <div class="sub-main right" style="width: 25%; height: 100%">
      <div class="container">
        <!-- <div class="paper-list-outer"><PaperList /></div>
        <div class="author-list-outer"><AuthorList /></div> -->
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
#paper-author {
  height: 30%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
#word-cloud{
  height: 30%;
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

