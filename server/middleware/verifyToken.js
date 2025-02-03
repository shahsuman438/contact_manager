const jwt=require('jsonwebtoken')



const jwt = require('jsonwebtoken');

function verifyToken(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ msg: "Unauthorized Access - No Token Provided" });
    }

    const token = authHeader.split(' ')[1];
    if (!token) {
        return res.status(401).json({ msg: "Unauthorized Access - Invalid Token" });
    }

    try {
        const payload = jwt.verify(token, process.env.ACCESS_TOKEN_SECRET);
        req.userId = payload.subject; // Ensure proper extraction of user ID
        next();
    } catch (error) {
        return res.status(403).json({ msg: "Forbidden - Invalid Token", error: error.name });
    }
}

module.exports = verifyToken;



module.exports=verifyToken