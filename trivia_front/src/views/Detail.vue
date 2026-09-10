<template>
  <div class="detail-page">
    <h1>No.{{ state.trivia.id }} {{ state.trivia.content }}</h1>
    <div class="explanation">
      {{ state.trivia.explanation ? state.trivia.explanation : "説明なし" }}
    </div>
    <div
      class="edit"
      v-if="state.trivia.userPost.id === userId"
      @click="edit()"
    >
      <img :src="require('@/assets/images/edit.png')" alt="編集" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, computed, PropType } from "vue";
import axios from "axios";
import { useStore } from "../store";
import { useRouter } from "../router";
import { TriviaModel } from "../types/task";

export default defineComponent({
  name: "detail",
  setup() {
    const store = useStore();
    const router = useRouter();

    const state = reactive({
      trivia: {
        id: Number,
        userPost: {
          id: Number,
          username: Number,
        },
        genre: {
          id: Number,
          name: String,
        },
        content: String,
        createdAt: String,
        explanation: String,
        goodCount: Number,
      },
    });
    const jwt = computed(() => {
      return store.getters.getToken;
    });
    const userId = computed(() => {
      return store.getters.getUserId;
    });
    onMounted(() => {
      axios
        .get(`api/trivias/${router.currentRoute.value.params.id}/`)
        .then((req) => {
          state.trivia = req.data;
        });
    });
    function edit() {
      router.push(`/edit/${router.currentRoute.value.params.id}`);
    }

    return { state, jwt, userId, edit };
  },
});
</script>

<style scoped>
.detail-page {
  position: relative;
  top: 100px;
  text-align: center;
}
.detail-page .explanation {
  border: black 2px dashed;
  width: 64%;
  margin: auto;
  text-align: left;
  height: 25em;
}
.detail-page .edit {
  cursor: pointer;
  position: absolute;
  right: 50px;
  top: 195px;
}
</style>
