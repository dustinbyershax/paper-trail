/**
 * Feedback page
 * Allows users to submit feedback about the application
 */
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export default function Feedback() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-3xl">Feedback</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600 mb-4">
          We value your feedback and suggestions!
        </p>
        <p className="text-gray-600">
          This feedback form is currently under development. For now, please contact
          us directly with any questions, comments, or suggestions about Paper Trail.
        </p>
      </CardContent>
    </Card>
  );
}
