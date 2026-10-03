<template>
  <div class="post-page">
    <div class="haiku-content">
      <label for="content">俳句</label>
      <textarea id="content" v-model="state.haikuContent"></textarea>
    </div>
    <div>
      <button @click="post()">投函</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, computed } from 'vue';
import { useStore } from '../store';
import { useRouter } from '../router';
import axios from 'axios';
export default defineComponent({
  setup() {
    const store = useStore();
    const router = useRouter();
    const state = reactive({
      haikuContent: '',
    });

    //JWT
    const jwt = computed(() => {
      return store.getters.getToken;
    });
    //投稿関数
    const post = () => {
      const data = {
        content: state.haikuContent,
      };
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `JWT ${jwt.value}`,
      };

      axios
        .post('/api/haikus/', data, {
          headers: headers,
        })
        .then((req) => {
          router.push(`/detail/${req.data.id}`);
        })
        .catch((err) => {
          console.error(err);
        });
    };
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
