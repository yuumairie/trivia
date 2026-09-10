export interface UserModel {
  id: number;
  username: string;
}

export interface TriviaModel {
  id: number;
  userPost: {
    id: number;
    username: string;
  };
  genre: {
    id: number;
    name: string;
  };
  content?: string;
  created_at?: string;
  explanation?: string;
  good?: Array<UserModel>
}

export interface GoodModel {
  id: number;
  user: string;
  trivia: string;
}



