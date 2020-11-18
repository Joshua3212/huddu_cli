<template>
  <div class="timestamp">
    <a
      href="#"
      class="bold"
      @click="currentTab = 1"
      :class="{ active: currentTab == 1 }"
      >1980</a
    >
    <a
      href="#"
      class="bold"
      @click="currentTab = 2"
      :class="{ active: currentTab == 2 }"
      >1990</a
    >
    <a
      href="#"
      class="bold"
      @click="currentTab = 3"
      :class="{ active: currentTab == 3 }"
      >2000</a
    >
    <a
      href="#"
      class="bold"
      @click="currentTab = 4"
      :class="{ active: currentTab == 4 }"
      >2010</a
    >
    <a
      href="#"
      class="bold"
      @click="currentTab = 5"
      :class="{ active: currentTab == 5 }"
      >2070</a
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentTab: 1,
    };
  },
};
</script>


<style scoped>
.timestamp {
  position: sticky;
  z-index: +1;
  width: 50px;
  height: 100vh;
  padding: 10px;
  padding-left: 20px;
  padding-right: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  background: rgb(255, 255, 255, 0.2);
  backdrop-filter: blur(2px);
}

a {
  color: black;
  text-decoration: none;
  padding: 10px;
  transition: 0.3s ease;
}

a:hover {
  color: white;
  background: #e73beb;
}
.active {
  color: white;
  transition: 0.3s ease;
  background: #e73beb;
}
</style>