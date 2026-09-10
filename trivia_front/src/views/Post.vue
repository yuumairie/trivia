<template>
  <div class="post-page">
    <div class="trivia-genre">
      <label for="genre">ジャンル</label>
      <select id="genre" v-model="state.genreId">
        <option
          v-for="genre in state.genreList"
          :key="genre.id"
          :value="genre.id"
          >{{ genre.name }}</option
        >
      </select>
    </div>
    <div class="trivia-content">
      <label for="content">内容</label>
      <textarea id="content" v-model="state.triviaContent"></textarea>
    </div>
    <div class="trivia-content">
      <label for="explanation">説明</label>
      <textarea id="explanation" v-model="state.triviaExplanation"></textarea>
    </div>
    <div>
      <button @click="post()">投函</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, computed, onMounted } from "vue";
import { useStore } from "../store";
import { useRouter } from "../router";
import axios from "axios";
export default defineComponent({
  setup() {
    const store = useStore();
    const router = useRouter();
    const state = reactive({
      genreList: [],
      genreId: "",
      triviaContent: "",
      triviaExplanation: "",
    });

    //JWT
    const jwt = computed(() => {
      return store.getters.getToken;
    });
    onMounted(() => {
      axios.get("api/genres/").then((req) => {
        state.genreList = req.data;
      });
    });
    //投稿関数
    function post() {
      const data = {
        genre: state.genreId,
        content: state.triviaContent,
        explanation: state.triviaExplanation,
      };
      const headers = {
        "Content-Type": "application/json",
        Authorization: `JWT ${jwt.value}`,
      };

      axios
        .post("api/trivias/", data, {
          headers: headers,
        })
        .then((req) => {
          router.push(`/detail/${req.data.id}`);
        });
    }
    return { state, post };
  },
});
</script>

<style scoped>
.post-page {
  position: relative;
  top: 100px;
}
</style>
