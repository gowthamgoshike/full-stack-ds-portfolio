import seaborn as sns
df=sns.load_dataset('titanic')
print(df[df['age']>10])
df['familysize']=df.groupby(('pclass','sex').transform)