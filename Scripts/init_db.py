
#show all user
@app.route('/user',methods=['GET'])
def getAllUser():
    all_users=User.query.all()
    result=user_schema.dump(all_users)
    return jsonify(result)