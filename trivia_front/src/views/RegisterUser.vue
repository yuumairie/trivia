<template>
  <div class="register-page">
    <label
      style="font-size:24px;background: linear-gradient(transparent 50%, #a8eaff 50%);"
    >
      アカウント情報を入力
    </label>
    <br />
    <br />
    <div class="info">
      <div>
        <label for="name">ユーザ名</label>
        <br />
        <input type="text" id="name" v-model="state.name" />
      </div>
      <br />
      <div>
        <label for="address">アドレス</label>
        <br />
        <input type="email" id="address" v-model="state.email" />
      </div>
      <br />
      <div>
        <label for="password">パスワード</label>
        <br />
        <input type="password" id="password" v-model="state.password" />
      </div>
      <br />
      <div>
        <button @click="create()">アカウント作成</button>
      </div>
      <br />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { useStore, ActionTypes } from "../store";
import { useRouter } from "../router";
import axios from "axios";
export default defineComponent({
  setup() {
    const state = reactive({
      name: "",
      email: "",
      password: "",
    });

    //アカウント作成関数
    function create() {
      const store = useStore();
      const router = useRouter();
      const data = {
        email: state.email,
        password: state.password,
        username: state.name
      };
      //アカウント作成
      axios.post("/api/register/", data).then(() => {
        //jwt取得
        store.dispatch(ActionTypes.LOGIN, data).then(() => {
          //ホーム画面へ移動
          router.push("home");
        });
      });
    }
    return { state, create };
  },
});
</script>

<style scoped>
.register-page .info {
  border: black 2px dashed;
  width: 64%;
  margin: auto;
}
.register-page {
  position: relative;
  top: 100px;
  text-align: center;
}
input {
  height: 1.5em;
  width: 17em;
}
</style>
