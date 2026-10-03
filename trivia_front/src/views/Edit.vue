<template>
  <div class="edit-page">
    <div class="trivia-genre">
      <label for="genre">ジャンル</label>
      <select id="genre" v-model="state.genreId">
        <option v-for="genre in state.genreList" :key="genre.id" :value="genre.id">
          {{ genre.name }}
        </option>
      </select>
    </div>
    <div class="trivia-content">
      <label for="content">内容</label>
      <textarea id="content" v-model="state.triviaContent" disabled="true"></textarea>
    </div>
    <div class="trivia-content">
      <label for="explanation">説明</label>
      <textarea id="explanation" v-model="state.triviaExplanation"></textarea>
    </div>
    <div>
      <button @click="update()">更新</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, computed, onMounted } from 'vue';
import { GenreModel } from '../types/task';
import { useStore } from '../store';
import { useRouter } from '../router';
import axios from 'axios';
export default defineComponent({
  setup() {
    const store = useStore();
    const router = useRouter();
    const state = reactive({
      genreList: [] as GenreModel[],
      genreId: '',
      triviaContent: '',
      triviaExplanation: '',
    });

    //JWT
    const jwt = computed(() => {
      return store.getters.getToken;
    });
    onMounted(() => {
      axios
        .get('/api/genres/')
        .then((req) => {
          state.genreList = req.data;
        })
        .catch((err) => {
          console.error(err);
        });
      axios
        .get(`api/trivias/${router.currentRoute.value.params.id}/`)
        .then((req) => {
          state.genreId = req.data.genre.id;
          state.triviaContent = req.data.content;
          state.triviaExplanation = req.data.explanation;
        })
        .catch((err) => {
          console.error(err);
        });
    });
    //更新関数
    const update = () => {
      const data = {
        genre: state.genreId,
        explanation: state.triviaExplanation,
      };
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `JWT ${jwt.value}`,
      };

      axios
        .patch(`api/trivias/${router.currentRoute.value.params.id}/`, data, {
          headers: headers,
        })
        .then(() => {
          router.push(`/detail/${router.currentRoute.value.params.id}`);
        })
        .catch((err) => {
          console.error(err);
        });
    };
    return { state, update, jwt };
  },
});
</script>

<style scoped>
.edit-page {
  position: relative;
  top: 100px;
}
</style>
