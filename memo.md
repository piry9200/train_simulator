# GeoPandasとShapelyの機能の使い分け

## 各データ型の抽出の仕方
あるGeoDataFrame「gdf」があり，中にsfデータを含む「geometry」列があるとする．

- gdf <- GeoDataFrame
- gdf.iloc[0] <- Pandas.Series
- gdf.iloc[[0]] <- GeopPandas.Series
- gdf.iloc[0]["geometry"] <- shapely.*　(多分．下の行との使い分けはとくにないか？)
- gdf.iloc[[0]]["geometry"] <- GeopPandas.Series(なんで？)

## GeoDataFrameの特徴，　メソッドやプロパティまとめ
- 座標系はこっちで管理する(shapelyの方では持てない？)
- 複数のsfをまとめて処理とかできる

## shapely.*のの特徴，　メソッドやプロパティまとめ
- sfを1つずつ処理できる

### 属性
- .xy(単体系): そのsfを構成する座標の一覧を返す．
- geoms(Mulit*系):形成する単体のsfをsequenceで返す

### メソッド
