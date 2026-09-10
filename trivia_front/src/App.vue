<template>
  <div class="root">
    <header id="nav">
      <h1 class="nav-bar" @click="goToHome()">
        <img
          style="height:20px"
          :src="require('@/assets/images/クラーケン.png')"
        />Uknown<img
          style="height:20px"
          :src="require('@/assets/images/ギャング.png')"
        />
      </h1>
      <div class="icons">
        <router-link to="/register">
          <div class="icon">
            <img
              style="height:20px"
              :src="require('@/assets/images/登録.png')"
            />
            新規登録
          </div></router-link
        >
        <router-link to="/login">
          <div class="icon">
            <img
              style="height:20px"
              :src="require('@/assets/images/ログイン.png')"
            />
            ログイン
          </div></router-link
        >
      </div>
    </header>
    <router-view />
    <div class="footer">
      Copyright © 2020 Inc. Co., Ltd., All Rights Unreserved.
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "../src/router";

export default defineComponent({
  setup() {
    function goToHome() {
      const router = useRouter();
      router.push("/home");
    }
    return { goToHome };
  },
});
</script>
<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#app #nav {
  position: fixed;
  background-color: floralwhite;
  color: black;
  text-align: left;
  height: 90px;
  background-image: url("../src/assets/images/brain-2029391_1280.png");
  width: 100%;
  margin: 0;
  top: 0;
  left: 0;
  border-bottom: black 2px solid;
  opacity: 0.9;
  z-index: 1030;
}
#nav .btn {
  background-color: white;
  color: black;
}
#nav .nav-bar {
  margin-top: 0;
  cursor: pointer;
  width: 200px;
  position: relative;
  top: 20px;
  left: 40px;
}
#nav .icon {
  width: 98px;
  margin-right: 15px;
}
#nav .icons {
  position: absolute;
  top: 60px;
  display: flex;
  right: 5px;
}
.footer {
  position: relative;
  top: 130px;
  height: 50px;
  background-color: aliceblue;
  padding-top: 26px;
  text-align: center;
}
</style>
