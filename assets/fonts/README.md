# フォントファイルについて

## 日本語フォントファイル配置場所

このディレクトリに日本語対応フォントファイルを配置すると、ゲーム内で自動的に使用されます。

## 推奨フォント

### 無料で使用可能な日本語フォント:
- **Noto Sans CJK JP**: Googleが開発したオープンソースフォント
  - ダウンロード: https://github.com/googlefonts/noto-cjk/releases
  - ファイル名例: `NotoSansCJK-Regular.ttc`

- **源ノ角ゴシック (Source Han Sans)**: Adobeが開発したオープンソースフォント  
  - ダウンロード: https://github.com/adobe-fonts/source-han-sans/releases
  - ファイル名例: `SourceHanSans-Regular.ttc`

## 使用方法

1. 上記フォントをダウンロード
2. `.ttf`, `.ttc`, `.otf`ファイルを `assets/fonts/` に配置
3. ゲームを再ビルド・実行

## ライセンス注意

- 商用利用する場合は各フォントのライセンスを確認してください
- このプロジェクトにフォントファイルは含まれていません（ライセンス問題回避）
- システムにインストール済みのフォントを優先的に使用します

## 対応システム

- **Windows**: メイリオ、MSゴシック等のシステムフォントを自動検出
- **macOS**: ヒラギノ角ゴシック等のシステムフォントを自動検出  
- **Linux**: Noto、DejaVu等のシステムフォントを自動検出