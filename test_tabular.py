from fastapi_backend.predictor import predict

print("Testing Heart Manual Entry...")
res_heart = predict('heart', form_data={'age': 55, 'chol': 220, 'bp': 120, 'hr': 80, 'maxhr': 140, 'st': 0, 'disease': 'heart'})
print("Heart Result:", res_heart)

print("Testing Diabetes Manual Entry...")
res_diab = predict('diabetes', form_data={'age': 55, 'preg': 2, 'glucose': 120, 'bp': 80, 'bmi': 25, 'insulin': 100, 'disease': 'diabetes'})
print("Diabetes Result:", res_diab)

print("Testing Heart CSV Entry...")
# create dummy csv
with open('test_heart.csv', 'w') as f:
    f.write('HighBP,HighChol,CholCheck,BMI,Smoker,Stroke,Diabetes,PhysActivity,Fruits,Veggies,HvyAlcoholConsump,AnyHealthcare,NoDocbcCost,GenHlth,MentHlth,PhysHlth,DiffWalk,Sex,Age,Education,Income\n')
    f.write('0,1,1,25,0,0,0,1,1,1,0,1,0,3,0,0,0,1,55,4,5\n')
res_heart_csv = predict('heart', file_path='test_heart.csv')
print("Heart CSV Result:", res_heart_csv)

print("Done")
