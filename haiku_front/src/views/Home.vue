<template>
  <div class="home">
    <div class="post" v-if="jwt">
      <router-link to="/post">投稿</router-link>
    </div>
    <div class="cards">
      <div v-for="haiku in state.haikuList" :key="haiku.id">
        <Haiku-Card
          :haiku="haiku"
          :isNotLoginUser="isNotLoginUser(haiku.userPost.id)"
          @get-haiku-list="getHaikuList"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, computed } from 'vue';
import axios from 'axios';
import HaikuCard from '../components/HaikuCard.vue';
import { useStore } from '../store';
import { HaikuModel } from '../types/task';
export default defineComponent({
  name: 'home',
  components: {
    HaikuCard,
  },
  setup() {
    const store = useStore();
    const state = reactive({
      haikuList: [] as HaikuModel[],
    });
    const jwt = computed(() => {
      return store.getters.getToken;
    });

    const getHaikuList = (): void => {
      axios
        .get('/api/haikus/')
        .then((req) => {
          state.haikuList = req.data;
        })
        .catch((err) => {
          console.error(err);
        });
    };

    onMounted(() => {
      getHaikuList();
    });
    const isNotLoginUser = (id: number): boolean => {
      if (jwt.value) {
        return store.getters.getUserId !== id;
      }
      return false;
    };

    return { state, jwt, isNotLoginUser, getHaikuList };
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
.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
