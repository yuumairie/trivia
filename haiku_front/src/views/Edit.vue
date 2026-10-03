<template>
  <div class="edit-page">
    <div class="haiku-content">
      <label for="content">俳句</label>
      <textarea id="content" v-model="state.haikuContent"></textarea>
    </div>
    <div>
      <button @click="update()">更新</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, computed, onMounted } from 'vue';
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
    onMounted(() => {
      axios
        .get(`api/haikus/${router.currentRoute.value.params.id}/`)
        .then((req) => {
          state.haikuContent = req.data.content;
        })
        .catch((err) => {
          console.error(err);
        });
    });
    //更新関数
    const update = () => {
      const data = {
        content: state.haikuContent,
      };
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `JWT ${jwt.value}`,
      };

      axios
        .patch(`api/haikus/${router.currentRoute.value.params.id}/`, data, {
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
