# 🧠 Pandas DataFramePlus

**DataFramePlus** is an extension of the popular pandas `DataFrame` class that helps you manage **correlated features** in your datasets.  
It warns you when you're about to drop a column that is **highly correlated** with another column that was **already dropped**, helping avoid unintended data loss during feature selection.

---

## 🚀 Features

- 📊 Drop-aware correlation tracking
- ⚠️ Warns on dropping the last correlated feature
- 🧪 Fully compatible with standard pandas operations
- 🔧 Customizable correlation tolerance

---

## 📦 Installation
To use `pandaspp` in your project:
```bash
git clone https://github.com/danielecursano/pandaspp.git
cd pandaspp
pip install -e .
```

---

## 💡 Usage example
```python
from pandaspp import DataFramePlus

df = DataFramePlus({
    "A": [1, 2, 3, 4],
    "B": [2, 4, 6, 8],   # Perfectly correlated with A
})

# Drop column A
df = df.drop(columns=["A"])

# Drop column B – this will warn you because B was highly correlated with A
df = df.drop(columns=["B"], raise_err=False)