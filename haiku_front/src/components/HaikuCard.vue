<template>
  <div class="haiku">
    <div class="content" @click="clickContent(haiku.id)">
      <div class="main">
        {{ haiku.content }}
      </div>
    </div>
    <div class="footer">
      <div class="user">
        {{ haiku.userPost.userName ? haiku.userPost.userName : '匿名' }}
      </div>
      <div class="time">{{ haiku.created_at }}</div>
      <div class="rap">
        <div class="heart" v-if="isNotLoginUser">
          <img
            class="heart-img"
            :src="require('@/assets/images/good.png')"
            @click="clickGood(false, haiku.id, haiku.good)"
            v-if="isAlreadyGood(haiku.good)"
          />
          <img
            class="heart-img"
            :src="require('@/assets/images/normal.png')"
            @click="clickGood(true, haiku.id)"
            v-else
          />
        </div>
      </div>
      <div>
        <p class="good">good</p>
        <div class="count">{{ haiku.good.length }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, reactive } from 'vue';
import { useRouter } from '../router';
import { ActionTypes, useStore } from '../store';
import axios from 'axios';
import { UserModel, GoodModel } from '../types/task.d';

export default defineComponent({
  name: 'HaikuCard',
  props: {
    haiku: {
      type: Object,
      required: true,
    },
    isNotLoginUser: Boolean,
  },
  emits: ['get-haiku-list'],
  setup(props, { emit }) {
    const router = useRouter();
    const store = useStore();
    const state = reactive({
      userId: store.getters.getUserId,
    });

    const goodList = computed<Array<GoodModel>>(() => {
      return store.getters.getGoodList;
    });

    const clickContent = (id: number) => {
      router.push(`/detail/${id}`);
    };

    const isAlreadyGood = (goodUserList: Array<UserModel>): boolean => {
      return goodUserList.some((user: UserModel) => {
        return user.id === state.userId;
      });
    };

    const getMyGood = (userId: string, haikuId: string): number => {
      const good: GoodModel | undefined = goodList.value.find((good) => {
        return good.user === userId && good.haiku === haikuId;
      });
      if (good) {
        return good.id;
      }
      return 0;
    };

    const clickGood = (isGood: boolean, id: string, goodUserList?: Array<UserModel>): void => {
      const data = {
        user: state.userId,
        haiku: id,
      };
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `JWT ${store.getters.getToken}`,
      };
      if (isGood) {
        axios
          .post('api/goods/', data, {
            headers: headers,
          })
          .then((resp) => {
            //ユーザのいいね一覧取得
            store.dispatch(ActionTypes.GOOD);
            emit('get-haiku-list');
          })
          .catch((err) => {
            console.error(err);
          });
      } else {
        axios
          .delete(`api/goods/${getMyGood(state.userId, id)}/`, {
            headers: headers,
          })
          .then((resp) => {
            //ユーザのいいね一覧取得
            store.dispatch(ActionTypes.GOOD);
            emit('get-haiku-list');
          })
          .catch((err) => {
            console.error(err);
          });
      }
    };
    return { clickContent, clickGood, isAlreadyGood };
  },
});
</script>

<style scoped>
.haiku {
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.16);
  border: solid black 1px;
  width: 320px;
  margin: 10px 30px 0px 30px;
  border-radius: 0 0 25px 25px;
}
.footer {
  border-radius: 0 0 25px 25px;
  height: 47px;
}
.haiku .user {
  position: relative;
  left: 50px;
  top: 11px;
}
.haiku .time {
  position: relative;
  bottom: 13px;
  left: 140px;
}
.haiku .content {
  text-align: center;
  cursor: pointer;
  overflow: hidden;
  border-bottom: 5px double;
}
.main {
  font-weight: bold;
  font-size: 25px;
  height: 130px;
  padding: 0 2px 0 2px;
}
.heart-img {
  height: 20px;
  position: relative;
  bottom: 35px;
  left: 249px;
  cursor: pointer;
}
.good {
  position: relative;
  bottom: 88px;
  left: 280px;
  font-size: 13px;
}
.count {
  position: relative;
  bottom: 104px;
  left: 292px;
  color: crimson;
  font-weight: bold;
}
.rap {
  min-height: 25px;
}
</style>
