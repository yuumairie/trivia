<template>
  <div class="login-page">
    <label
      style="font-size:24px;background: linear-gradient(transparent 50%, #a8eaff 50%);"
    >
      ログイン
    </label>
    <br /><br />
    <div class="info">
      <div class="email">
        <label for="address">アドレス</label>
        <br />
        <input type="email" id="address" v-model="state.email" />
      </div>
      <br />
      <div class="password">
        <label for="password">パスワード</label>
        <br />
        <input type="password" id="password" v-model="state.password" />
      </div>
      <br />
      <div>
        <button @click="login()">ログイン</button>
      </div>
      <br />
      <div class="message" v-if="state.message">
        {{ state.message }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { useStore, ActionTypes } from "../store";
import { useRouter } from "../router";

export default defineComponent({
  setup() {
    const state = reactive({
      name: "",
      email: "",
      password: "",
      message: "",
    });

    //ログイン
    function login() {
      const store = useStore();
      const router = useRouter();
      const data = {
        email: state.email,
        password: state.password,
      };

      //jwt取得
      store
        .dispatch(ActionTypes.LOGIN, data)
        .then((resp) => {
          //ユーザのいいね一覧取得
          store.dispatch(ActionTypes.GOOD)
          //ホーム画面へ移動
          router.push("home");
        })
        .catch(() => {
          state.message = "メールアドレスかパスワードが違います。";
        });
    }
    return { state, login };
  },
});
</script>

<style scoped>
.login-page {
  position: relative;
  top: 100px;
  text-align: center;
}
input {
  height: 1.5em;
  width: 17em;
}
.info {
  border: black 2px dashed;
  width: 64%;
  margin:auto;
}
</style>
