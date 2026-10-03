<template>
  <div class="detail-page">
    <h1>No.{{ state.haiku.id }} {{ state.haiku.content }}</h1>
    <div class="edit" v-if="state.haiku.userPost.id === userId" @click="edit()">
      <img :src="require('@/assets/images/edit.png')" alt="編集" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, computed } from 'vue';
import axios from 'axios';
import { useStore } from '../store';
import { useRouter } from '../router';

export default defineComponent({
  name: 'detail',
  setup() {
    const store = useStore();
    const router = useRouter();

    const state = reactive({
      haiku: {
        id: Number,
        userPost: {
          id: Number,
          username: Number,
        },
        content: String,
        createdAt: String,
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
        .get(`api/haikus/${router.currentRoute.value.params.id}/`)
        .then((req) => {
          state.haiku = req.data;
        })
        .catch((err) => {
          console.error(err);
        });
    });
    const edit = () => {
      router.push(`/edit/${router.currentRoute.value.params.id}`);
    };

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
.detail-page .edit {
  cursor: pointer;
  position: absolute;
  right: 50px;
  top: 195px;
}
</style>
