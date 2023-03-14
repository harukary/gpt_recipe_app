import tiktoken,re,json,requests,bs4,easyocr
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import matplotlib.patches as patches
import japanize_matplotlib

from core.chatgpt import ChatGPT

class RecipeImporter:
    json_pattern = r'\{.*\}'
    recipe_json_tokens = 1750
    def __init__(
            self,
            recipe_format_path='../setting/recipe_format.json'
        ):
        self.recipe_format = open(recipe_format_path, 'r').read()
        self.setting = '以下のJson形式に基づいて、レシピJsonを出力してください。数値がわからない場合は、nullとしてください。\n'+ self.recipe_format + '\n\n'
        self.enc = tiktoken.get_encoding("gpt2")
        self.ocr = easyocr.Reader(['ja','en'], gpu=True)
        self.chatgpt = ChatGPT(
            max_tokens=self.recipe_json_tokens,
            temperature=0.1,
            setting=self.setting
        )
    
    def text_to_recipe(self,text):
        messages = [
            {"role": "system", "content": self.setting},
            {"role": "user", "content": text},
        ]
        res = self.chatgpt.complete(messages)
        match = re.search(self.json_pattern, res, re.DOTALL)
        if match:
            json_string = match.group()
            recipe_json = json.loads(json_string)
            return recipe_json
        else:
            print('Error:',res)
            return {}

    def recipe_to_recipe(self,recipe):
        recipe_text = json.dumps(recipe,ensure_ascii=False) + '\nnullとなっている部分は推定して補完してください。'
        return self.text_to_recipe(recipe_text)
    
    def url_to_recipe(self,url,start=None,end=None):
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        recipe_text = soup.get_text().replace('\n\n','')
        # 文字数制限があるため、不要部分をカット
        if start is not None:
            recipe_text = recipe_text[recipe_text.find(start):]
        if end is not None:
            recipe_text = recipe_text[:recipe_text.find(end)]
        return self.text_to_recipe(recipe_text)

    def image_to_recipe(self,image_path):
        recipe_text = self.image_to_text(image_path,viz=True)
        return self.text_to_recipe(recipe_text)
    
    def image_to_text(self,image_path,viz=False):
        res = self.ocr.readtext(image_path)
        clustered_res = self.cluster_ocr_results(res)
        if viz:
            self.viz_ocr_results(image_path, clustered_res)
        clusters = {}
        for r in clustered_res:
            if r['label'] not in clusters.keys():
                clusters[r['label']] = []
            clusters[r['label']].append(r)
        recipe_text = ''
        for label,cluster in clusters.items():
            for c in cluster:
                recipe_text += c['text']+'\n'
            recipe_text += '\n'
        return recipe_text

    def cluster_ocr_results(self, ocr_results, eps=0.4, min_samples=2):
        # Bounding boxの中心座標とテキスト情報を計算してデータを作成
        centers = []
        texts = []
        confidences = []
        for i, result in enumerate(ocr_results):
            box = result[0]
            center = np.mean(box, axis=0)
            centers.append(center)
            texts.append(result[1])
            confidences.append(result[2])
        X = StandardScaler().fit_transform(centers)

        # DBSCANによるクラスタリング
        dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(X)

        # クラスタリング結果と各クラスタに含まれるテキスト情報の出力
        labels = dbscan.labels_
        # print(set(labels))
        clusters = []
        for label, result in zip(labels, ocr_results):
            result_dict = {'box': result[0], 'text': result[1], 'confidence': result[2], 'label': label}
            clusters.append(result_dict)
        return clusters

    def viz_ocr_results(self,image_path, ocr_results):
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink']
        image = Image.open(image_path)
        fig = plt.figure(figsize = (8,12))
        ax = plt.axes()
        ax.imshow(image)
        ax.axis("off")
        for t in ocr_results:
            try:
                bbox = np.array(t['box'])
                # print(bbox)
                ax.text(bbox[3,0], bbox[3,1], t['text'], size=5,color="black")
                r = patches.Rectangle(
                    xy=(bbox[0,0], bbox[0,1]), width=(bbox[2,0] - bbox[0,0]), height=(bbox[2,1] - bbox[0,1]), 
                    ec=colors[t['label']], fill=False,linewidth=1.0
                )
                ax.add_patch(r)
            except:
                continue
        plt.savefig(image_path.replace('.png','_ocr.png').replace('.jpg','_ocr.jpg'))