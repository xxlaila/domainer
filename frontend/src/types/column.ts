export type ColumnItem<T> = {
  key: keyof T | 'action';
  label: string;
  width?: number;
  minWidth?: number;
  link?: boolean;
  /*
   * @description 当前项是否是自定义slot
   * @type {boolean}
   * */
  slot?: boolean;
  fixed?: string;
  ellipsis?: boolean;
};

export type ColumnLists<T> = ColumnItem<T>[];
