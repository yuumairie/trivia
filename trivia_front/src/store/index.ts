import { createStore, MutationTree, ActionContext, ActionTree, GetterTree, Store as VuexStore, CommitOptions, DispatchOptions, createLogger } from 'vuex'
import axios from 'axios'
import { GoodModel } from '../types/task.d'

export type State = {
  name: string;
  email: string;
  jwt: string;
  userId: number;
  goodList: Array<GoodModel>;
}
const state: State = {
  name: "",
  email: "",
  jwt: "",
  userId: 0,
  goodList: []
}

export enum MutationTypes {
  LOGIN = "LOGIN",
  GOOD = "GOOD",
}
export enum ActionTypes {
  LOGIN = "LOGIN",
  GOOD = "GOOD",
}

export type Mutations<S = State> = {
  [MutationTypes.LOGIN](state: S, payload: string): void;
  [MutationTypes.GOOD](state: S, payload: Array<GoodModel>): void;
}

const mutations: MutationTree<State> & Mutations = {
  // login mutation
  [MutationTypes.LOGIN](state: State, payload: string) {
    state.jwt = payload;
    const headers = {
      "Content-Type": "application/json",
      Authorization: `JWT ${payload}`
    }
    axios.get("api/myprofile/", {
      headers: headers
    }).then((res) => {
      state.userId = res.data[0].id
    })
  },

  // good mutation
  [MutationTypes.GOOD](state: State, payload: Array<GoodModel>) {
    state.goodList = payload
  }

}

type AugmentedActionContext = {
  commit<k extends keyof Mutations>(
    key: k,
    payload: Parameters<Mutations[k]>[1]
  ): ReturnType<Mutations[k]>;
} & Omit<ActionContext<State, State>, "commit">

export interface Actions {
  [ActionTypes.LOGIN](
    { commit }: AugmentedActionContext,
    payload: {
      email: string;
      password: string;
    }
  ): void;

  [ActionTypes.GOOD](
    { commit }: AugmentedActionContext
  ): void;
}

export const actions: ActionTree<State, State> & Actions = {
  // login action
  [ActionTypes.LOGIN]({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios.post("authen/jwt/create", data).then((res) => {
        commit(MutationTypes.LOGIN, res.data.access)
        resolve(res.data.access)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  // good action
  [ActionTypes.GOOD]({ commit }) {
    const headers = {
      "Content-Type": "application/json",
      Authorization: `JWT ${state.jwt}`
    }
    axios.get("api/goods/", {
      headers: headers
    }).then((res) => {
      commit(MutationTypes.GOOD, res.data)
    })
  },


}
export type Getters = {
  getToken(state: State): string;
  getUserId(state: State): number;
  getGoodList(state: State): Array<GoodModel>;
}

export const getters: GetterTree<State, State> & Getters = {
  getToken: state => {
    return state.jwt
  },
  getUserId: state => {
    return state.userId
  },
  getGoodList: state => {
    return state.goodList
  }
}

export type Store = Omit<
  VuexStore<State>,
  "commit" | "getters" | "dispatch"
> & {
  commit<k extends keyof Mutations, P extends Parameters<Mutations[k]>[1]>(
    key: k,
    payload: P,
    options?: CommitOptions
  ): ReturnType<Mutations[k]>;
} & {
  getters: {
    [K in keyof Getters]: ReturnType<Getters[K]>;
  };
} & {
  dipatch<K extends keyof Actions>(
    key: K,
    payload: Parameters<Actions[K]>[1],
    options?: DispatchOptions
  ): ReturnType<Actions[K]>;
}

export const store = createStore({
  state,
  mutations,
  actions,
  getters,
  plugins: [createLogger()]
})

export function useStore() {
  return store;
}




