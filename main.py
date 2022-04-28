from website import create_app

app = create_app()

if __name__ == '__main__':
    #Secret Key!(This added because of Flash messages)
    app.secret_key='my super secret key'
    # dubug=true makes server refresh after making changes
    # in code without a need of stopping/restarting the server
    app.run(debug=True)