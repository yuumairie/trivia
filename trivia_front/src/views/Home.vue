<template>
  <div class="home">
    <div class="post" v-if="jwt">
      <router-link to="/post">投稿</router-link>
    </div>
    <div class="search">
      <select id="genre" v-model="state.genreId">
        <option
          v-for="genre in state.genreList"
          :key="genre.id"
          :value="genre.id"
          >{{ genre.name }}</option
        >
      </select>
      <img
        class="glasses"
        :src="require('@/assets/images/虫眼鏡.png')"
        alt="検索"
        @click="search()"
      />
    </div>
    <div class="cards">
      <div v-for="trivia in triviaOnSearch" :key="trivia">
        <Trivia-Card
          :trivia="trivia"
          :isNotLoginUser="isNotLoginUser(trivia.userPost.id)"
          @get-trivia-list="getTriviaList"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, computed } from "vue";
import axios from "axios";
import TriviaCard from "../components/TriviaCard.vue";
import { useStore } from "../store";
import { useRouter } from "../router";
import { TriviaModel } from "../types/task";
export default defineComponent({
  name: "home",
  components: {
    TriviaCard,
  },
  setup() {
    const store = useStore();
    const state = reactive({
      triviaList: [],
      genreList: [],
      genre: 0,
      genreId: 0,
    });
    const jwt = computed(() => {
      return store.getters.getToken;
    });
    const triviaOnSearch = computed(() => {
      if (state.genre) {
        return state.triviaList.filter((trivia: TriviaModel) => {
          return trivia.genre.id === state.genre;
        });
      }
      return state.triviaList;
    });

    function getTriviaList(): void {
      axios.get("api/trivias/").then((req) => {
        state.triviaList = req.data;
      });
    }

    onMounted(() => {
      getTriviaList();
      axios.get("api/genres/").then((req) => {
        state.genreList = req.data;
      });
    });
    function search(): void {
      state.genre = state.genreId;
    }
    function isNotLoginUser(id: number): boolean {
      if (jwt.value) {
        return store.getters.getUserId !== id;
      }
      return false;
    }

    return { state, jwt, search, triviaOnSearch, isNotLoginUser ,getTriviaList};
  },
});
</script>
<style scoped>
.home {
  position: relative;
  top: 100px;
}
.post {
  float: right;
}
.glasses {
  width: 20px;
  margin-left: 18px;
  cursor: pointer;
}
.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.search {
  text-align: center;
}
</style>
