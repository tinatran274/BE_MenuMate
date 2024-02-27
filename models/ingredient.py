from extension import db, ma 

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    removal = db.Column(db.Integer, nullable=False)
    kcal = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    lipid = db.Column(db.Float, nullable=False)
    glucid = db.Column(db.Float, nullable=False)
    canxi = db.Column(db.Float, nullable=False)
    phosphor = db.Column(db.Float, nullable=False)
    fe = db.Column(db.Float, nullable=False)
    vitamin_a = db.Column(db.Float, nullable=False)
    beta_caroten = db.Column(db.Float, nullable=False)
    vitamin_b1 = db.Column(db.Float, nullable=False)
    vitamin_b2 = db.Column(db.Float, nullable=False)
    vitamin_pp = db.Column(db.Float, nullable=False)
    vitamin_c = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    def __init__(self, name, removal, kcal, protein, lipid, glucid, canxi, phosphor, fe,
                 vitamin_a, beta_caroten, vitamin_b1, vitamin_b2, vitamin_pp, vitamin_c, category):
        self.name = name
        self.removal = removal
        self.kcal = kcal
        self.protein = protein
        self.lipid = lipid
        self.glucid = glucid
        self.canxi = canxi
        self.phosphor = phosphor
        self.fe = fe
        self.vitamin_a = vitamin_a
        self.beta_caroten = beta_caroten
        self.vitamin_b1 = vitamin_b1
        self.vitamin_b2 = vitamin_b2
        self.vitamin_pp = vitamin_pp
        self.vitamin_c = vitamin_c
        self.category = category

    def __repr__(self):
        return f'<Ingredient {self.name}>'
    

class IngredientSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'name',
            'removal',
            'kcal',
            'protein',
            'lipid',
            'glucid',
            'canxi',
            'phosphor',
            'fe',
            'vitamin_a',
            'beta_caroten',
            'vitamin_b1',
            'vitamin_b2',
            'vitamin_pp',
            'vitamin_c',
            'category'
        )