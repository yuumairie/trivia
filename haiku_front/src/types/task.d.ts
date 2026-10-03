export interface UserModel {
  id: number;
  username: string;
}

export interface HaikuModel {
  id: number;
  userPost: {
    id: number;
    username: string;
  };
  content?: string;
  created_at?: string;
  good?: Array<UserModel>;
}

export interface GoodModel {
  id: number;
  user: string;
  haiku: string;
}
