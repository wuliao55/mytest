import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
# ====================== 1. 加载并查看数据 ======================
# 确保insurance.csv和此文件在同一目录（D:\streamlit_env\）
data = pd.read_csv('insurance.csv')
# 查看数据集结构（可选，用于确认字段）
print("数据集字段：", data.columns.tolist())
print("数据集前5行：")
print(data.head())
# 特征（X）：age, sex, bmi, children, smoker, region
# 目标（y）：charges（医疗费用）
X = data[['age', 'sex', 'bmi', 'children', 'smoker', 'region']]
y = data['charges']
# ====================== 2. 手动对分类特征做独热编码（和前端对齐） ======================
# 分类特征：sex（男性/女性）、smoker（是/否）、region（东南部/西南部/东北部/西北部）
# 步骤：将分类特征转换为独热编码（和前端代码的编码逻辑完全一致）
# 2.1 性别独热编码（sex_female, sex_male）
X = pd.get_dummies(X, columns=['sex'], prefix='sex', drop_first=False)
# 2.2 吸烟状态独热编码（smoker_yes, smoker_no）
X = pd.get_dummies(X, columns=['smoker'], prefix='smoker', drop_first=False)
# 2.3 区域独热编码（region_东南部, region_西南部, region_东北部, region_西北部）
# 注意：数据集里的region是英文（southeast/southwest/northeast/northwest），需和前端中文对应
# 先将数据集的英文region替换为中文（和前端一致）
X['region'] = X['region'].map({
    'southeast': '东南部',
    'southwest': '西南部',
    'northeast': '东北部',
    'northwest': '西北部'
})
X = pd.get_dummies(X, columns=['region'], prefix='region', drop_first=False)
# 查看编码后的特征（关键！记录特征名和顺序）
print("\n编码后的特征名：", X.columns.tolist())
print("编码后的特征数量：", len(X.columns.tolist()))
# ====================== 3. 拆分训练集和测试集 ======================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# ====================== 4. 训练随机森林模型 ======================
rfr_model = RandomForestRegressor(n_estimators=100, random_state=42)
rfr_model.fit(X_train, y_train)
# ====================== 5. 保存模型和特征名（关键！前端需要用） ======================
# 保存模型
with open('rfr_model.pkl', 'wb') as f:
    pickle.dump(rfr_model, f)
# 保存特征名（后续前端代码直接用这个列表）
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)
print("\n模型和特征名已保存！")
print("最终特征名列表：", X.columns.tolist())
